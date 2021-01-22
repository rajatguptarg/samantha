#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""


import logging

from samantha.sender import SlackWebClient
from samantha.brain.command_factory import CommandFactory


__all__ = ['ResponderMessageProcessor']

logger = logging.getLogger(__name__)


class ResponderMessageProcessor(object):
    """
    Process the response returned by Responder
    """
    def __init__(self):
        self.sender = SlackWebClient()
        self.factory = CommandFactory()

    def process(self, response, channel, user):
        """
        Process responder's response
        """
        logger.info("Recieved responder response: %s" % ((response)))
        if not response:
            text = str(response) + "\nI can not perform this yet. This is coming soon!"
            return self.sender.send_text(text=text, channel=channel)
        command = self.factory.get_command(response, channel, user)
        return command.execute()
