#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import uuid
import json
import logging
from subprocess import Popen, PIPE
from abc import ABCMeta, abstractmethod, ABC

from samantha.sender import Sender
from samantha import config
from iaac import AnsibleService


__all__ = ['BotCommand']

logger = logging.getLogger(__name__)


class BotCommand(ABC):
    """
    Command Object which is being inherited by the all the commands
    which are being executed by the bot.
    """
    __metaclass__ = ABCMeta

    def __init__(self, channel, user, send_mediums=['slack']):
        self.result_start = '{\n    "custom_stats"'
        self.sender = Sender()
        self.channel = channel
        self.user = user
        self.send_mediums = send_mediums
        opts = config.get_ansible_config()
        self._sources = opts.inventory_file + 'dev'
        self.ansible_service = AnsibleService()
        super(BotCommand, self).__init__()

    @abstractmethod
    def execute(self):
        pass

    def generate_uuid(self):
        """
        Returns the string UUID
        """
        return str(uuid.uuid1())

    def run_command(self, command: str, cwd: str, env: dict, shell=True):
        """
        Run the shell commands
        """
        process = Popen(
            [command], shell=shell, cwd=cwd, env=env, stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8")
        error = stderr.decode("utf-8")
        rc = process.returncode
        logger.info("Finished command: %s with rc %s." % (str(command), str(rc)))
        return (output, error, rc)

    def parse_stdout_to_json(self, output):
        """
        Parse the output to json
        """
        try:
            res_index = output.find(self.result_start)
            res_str = output[res_index:]
            return json.loads(res_str)
        except:
            res_str = '{"status": "parsing failed."}'
            return json.loads(res_str)
