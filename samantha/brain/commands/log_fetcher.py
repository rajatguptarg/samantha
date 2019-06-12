#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

from samantha.brain.commands.command import Command


__all__ = ['LogFetcher']


class LogFetcher(Command):
    """
    Log class for log fetching
    """
    def __init__(self, text, channel):
        self.text = text
        self.channel = channel
        super(LogFetcher, self).__init__()

    def execute(self):
        """
        Command Executioner
        """
        return self.sender.send_text(
                text=self.text, channel=self.channel)
