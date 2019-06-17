#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import configargparse
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
        parser = configargparse.get_argument_parser()
        parser.add_argument(
            '-i', '--ansible-inventory-file', dest='ansible_inventory_file',
            env_var='ANSIBLE_INVENTORY_FILE', help='Path for ansible inventory files'
        )
        opts = parser.parse_known_args()[0]
        self._sources = opts.ansible_inventory_file + 'dev'
        self.ansible_service = AnsibleService()
        super(BotCommand, self).__init__()

    @abstractmethod
    def execute(self):
        pass
