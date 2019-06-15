#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import os
from abc import ABCMeta, abstractmethod, ABC

from samantha.sender import Sender
from iaac import AnsibleService


__all__ = ['BotCommand']


class BotCommand(ABC):
    """
    Command Object which is being inherited by the all the commands
    which are being executed by the bot.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.sender = Sender()
        self._sources = os.getenv('ANSIBLE_INVENTORY_FILE')
        self.ansible_service = AnsibleService()
        super(BotCommand, self).__init__()

    @abstractmethod
    def execute(self):
        pass
