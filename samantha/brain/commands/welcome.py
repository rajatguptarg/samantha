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
    name = 'welcome'

    def __init__(self, response, channel, user):
        super(Welcome, self).__init__(channel, user)
        self.response = response

    def execute(self):
        """
        Command Executioner
        """
        text = self.response.query_result.fulfillment_text
        return self.sender.slack_client.send_text(
                text=text, channel=self.channel)
