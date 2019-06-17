#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""


from samantha.brain.commands.command import BotCommand


__all__ = ['Welcome']


class Welcome(BotCommand):
    """
    Command class for Welcome messages
    """
    def __init__(self, text, channel):
        self.text = text
        self.channel = channel
        super(Welcome, self).__init__()

    def execute(self):
        """
        Command Executioner
        """
        return self.sender.slack_client.send_text(
                text=self.text, channel=self.channel)
