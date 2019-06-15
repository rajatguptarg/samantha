#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import json

from iaac.tasks import Debug
from iaac.tasks import Command
from iaac import ResultCallback

from samantha.brain.commands.command import BotCommand
from google.protobuf.json_format import MessageToDict


__all__ = ['LogFetcher']


class LogFetcher(BotCommand):
    """
    Log class for log fetching
    """
    QUICK_REPLY = 'I am on it. I will send you the file once I am done'

    def __init__(self, response, channel):
        self.data = MessageToDict(response)
        self.channel = channel
        self.callback = LogFetcherCallback(self.channel)
        super(LogFetcher, self).__init__()

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
        task_1 = Command(argv=['ls', '-lah'], chdir='/home/rajat', register='shell_out')
        task_2 = Debug(msg='{{shell_out.stdout}}')
        return [task_1.action(), task_2.action()]

    def execute(self):
        """
        Command Executioner
        """
        self.ansible_service.initialize(
            self._sources, self.servers, self._build_ansible_tasks(), self.callback
        )
        self.sender.slack_client.send_text(text=self.QUICK_REPLY, channel=self.channel)
        return self.ansible_service.run()


class LogFetcherCallback(ResultCallback):
    """
    Callback plugin for ansible

    Inherits all the default behaviour of ansible callback
    """
    def __init__(self, channel):
        self.channel = channel
        super(LogFetcherCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        return self.sender.slack_client.send_text(
            text=(json.dumps({host.name: result._result}, indent=4)),
            channel=self.channel
        )
