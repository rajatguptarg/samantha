#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

from iaac.tasks import Command
from iaac import ResultCallback

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
        super(LogFetcher, self).__init__()
        self.user = user
        self.data = MessageToDict(response)
        self.channel = channel
        opts = config.get_ansible_config()
        command_config = config.get_command_setting(self.name)
        self.log_file_map = command_config['log_file_map']
        self.send_mediums = command_config['send_via']
        self.inventory_file_path = opts.inventory_file

    @property
    def environment(self):
        return self.data['queryResult']['parameters']['env']

    @property
    def servers(self):
        return self.data['queryResult']['parameters']['servers'][0]

    @property
    def fileage(self):
        return self.data['queryResult']['parameters']['day']

    def _build_ansible_tasks(self):
        try:
            filename = self.log_file_map.get(self.servers).get(self.environment)
        except:
            filename = '/var/log/syslog'
        task_1 = Command(argv=['cat', filename])
        return [task_1.action()]

    def execute(self):
        """
        Command Executioner
        """
        self.callback = LogFetcherCallback(self.channel, self.send_mediums, self.user)
        self._sources = self.inventory_file_path + self.environment
        self.sender.slack_client.send_text(text=self.QUICK_REPLY, channel=self.channel)
        self.ansible_service.initialize(
            self._sources, self.servers, self._build_ansible_tasks(), self.callback
        )
        return self.ansible_service.run()


class LogFetcherCallback(ResultCallback):
    """
    Callback plugin for ansible

    Inherits all the default behaviour of ansible callback
    """
    def __init__(self, channel, send_mediums, user):
        super(LogFetcherCallback, self).__init__()
        self.channel = channel
        self.user = user
        self.send_mediums = send_mediums
        self.email_subject = "Request for Log Files"
        self.default_body = "Please see the attached logs"
        self.recipient = self.user.profile.email

    def v2_runner_on_ok(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        output = result._result.get('stdout', '')
        filename = host.name + '.log'
        if 'slack' in self.send_mediums:
            self._send_via_slack(output, filename)
        if 'email' in self.send_mediums:
            self._send_via_email(output, filename)

    def _send_via_slack(self, output, filename):
        """
        Send message via slack
        """
        self.sender.slack_client.send_text_as_file(
            content=output, channel=self.channel, filename=filename,
            filetype='text', title=filename
        )

    def _send_via_email(self, output, filename):
        """
        Send message via emails
        """
        message = self.sender.email_client.build_email(
            recipient=self.recipient, subject=self.email_subject,
            text=self.default_body, file_content=output, filename=filename
        )
        self.sender.email_client.send(self.recipient, message)
