#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

from iaac.tasks import Command
from iaac import ResultCallback

from subprocess import Popen, PIPE

from samantha import config
from samantha.brain.commands.command import BotCommand
from google.protobuf.json_format import MessageToDict


__all__ = ['LogFetcher']


class LogFetcher(BotCommand):
    """
    Log class for log fetching

    In case of, adding more servers with log files, please add server
    wrt each environemts in the log_file_map in application config
    """
    name = 'log_fetcher'
    QUICK_REPLY = 'I am on it. I will send you the file once I am done'

    def __init__(self, response, channel, user):
        super(LogFetcher, self).__init__(channel, user)
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

    def execute(self):
        """
        Command Executioner
        """
        filename = 'output'
        playbook = self.command_config.get('playbook_map').get(self.server)
        command = 'ansible-playbook -i ' + \
            self.inventory_file_path + self.environment + ' ' + playbook

        process = Popen(
            [command], shell=True, cwd=self.iaac_path,
            stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")

        if 'slack' in self.send_mediums:
            self.sender.slack_client.send_text_as_file(
                content=output, channel=self.channel, filename=filename,
                filetype='text', title=filename
            )
        if 'email' in self.send_mediums:
            message = self.sender.email_client.build_email(
                recipient=self.recipient, subject=self.email_subject,
                text=self.default_body, file_content=output, filename=filename
            )
            self.sender.email_client.send(self.recipient, message)
