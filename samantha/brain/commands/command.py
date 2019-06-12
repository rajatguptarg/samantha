#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""


from abc import ABCMeta, abstractmethod, ABC

from samantha.sender import SlackWebClient


__all__ = ['Command']


class Command(ABC):
    """
    Command Object which is being inherited by the all the commands
    which are being executed by the bot.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.sender = SlackWebClient()
        super(Command, self).__init__()

    @abstractmethod
    def execute(self):
        pass
