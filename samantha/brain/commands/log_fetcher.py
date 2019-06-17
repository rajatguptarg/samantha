#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import os

from iaac.tasks import Command
from iaac import ResultCallback

from samantha.brain.commands.command import BotCommand
from google.protobuf.json_format import MessageToDict


__all__ = ['LogFetcher']


class LogFetcher(BotCommand):
    """
    Log class for log fetching

    In case of, adding more servers with log files, please add server
    wrt each environemts in the LOG_FILE_MAP
    """
    QUICK_REPLY = 'I am on it. I will send you the file once I am done'

    LOG_FILE_MAP = {
        'rts': {
            'prod': '/var/log/erlnoc/live/console.log',
            'staging': '/var/log/erlnoc/pilot/console.log',
            'qa': '/var/log/erlnoc/sim_ops/console.log',
            'dev': '/var/log/erlnoc/sim_ops/console.log',
        },
    }

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
        try:
            filename = self.LOG_FILE_MAP.get(self.servers).get(self.environment)
        except:
            filename = '/var/log/syslog'
        task_1 = Command(argv=['cat', filename])
        return [task_1.action()]

    def execute(self):
        """
        Command Executioner
        """
        self._sources = os.getenv('ANSIBLE_INVENTORY_FILE') + self.environment
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
    def __init__(self, channel):
        self.channel = channel
        super(LogFetcherCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        output = result._result.get('stdout', '')
        filename = host.name + '.txt'
        return self.sender.slack_client.send_text_as_file(
            content=output, channel=self.channel, filename=filename,
            filetype='text', title=filename
        )
