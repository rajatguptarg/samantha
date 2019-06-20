#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

from abc import ABCMeta, abstractmethod, ABC

from samantha.sender import Sender
from samantha import config
from iaac import AnsibleService


__all__ = ['BotCommand']


class BotCommand(ABC):
    """
    Command Object which is being inherited by the all the commands
    which are being executed by the bot.
    """
    __metaclass__ = ABCMeta

    def __init__(self, channel, user, send_mediums=['slack']):
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
