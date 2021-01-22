#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import os
# import json
import logging

from samantha import config
from samantha.brain.commands.command import BotCommand
from google.protobuf.json_format import MessageToDict


__all__ = ['MPStat']

logger = logging.getLogger(__name__)


class MPStat(BotCommand):
    """
    Log class for log fetching

    In case of, adding more servers with log files, please add server
    wrt each environemts in the log_file_map in application config
    """
    name = 'mpstat'
    QUICK_REPLY = 'I am on it. I will send you the file once I am done'

    def __init__(self, response, channel, user):
        super(MPStat, self).__init__(channel, user)
        self.data = MessageToDict(response)
        opts = config.get_ansible_config()
        self.command_config = config.get_command_setting(self.name)
        self.iaac_path = opts.home_location
        self.send_mediums = self.command_config['send_via']
        self.inventory_file_path = opts.inventory_file
        self.email_subject = "Request for Log Files"
        self.default_body = "Please see the attached logs"
        self.recipient = self.user.profile.email

    @property
    def environment(self):
        return self.data['queryResult']['parameters']['env']

    @property
    def server(self):
        return self.data['queryResult']['parameters']['servers'][0]

    @property
    def fileage(self):
        return self.data['queryResult']['parameters']['day']

    def _get_command(self):
        """
        Returns the ansible command
        """
        # playbook = self.command_config.get('playbook_map').get(self.server)
        # command = 'ansible-playbook -i ' + \
        #     self.inventory_file_path + self.environment + ' ' + playbook
        # return command
        return "ansible-playbook -i inventory/prod -e env=prod \
            -e hname=localhost fetch-ansible-log-file.yml"

    def execute(self):
        """
        Command Executioner
        """
        filename = 'output'
        task_id = self.generate_uuid()
        env_vars = os.environ.copy()
        env_vars.update({'task_id': task_id})
        command = self._get_command()
        logger.info("Running command: %s with task id %s." % (str(command), task_id))

        output, error, rc = self.run_command(
            command=command, cwd=self.iaac_path, env=env_vars)
        json_output = self.parse_stdout_to_json(output)
        str_output = json_output.get('plays')[0]['localhost']['stdout']

        if 'slack' in self.send_mediums:
            self.sender.slack_client.send_text_as_file(
                content=str_output, channel=self.channel, filename=filename,
                filetype='json', title=filename
            )
        if 'email' in self.send_mediums:
            message = self.sender.email_client.build_email(
                recipient=self.recipient, subject=self.email_subject,
                text=self.default_body, file_content=str_output, filename=filename
            )
            self.sender.email_client.send(self.recipient, message)
