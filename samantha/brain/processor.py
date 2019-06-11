#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""


import logging

from samantha.sender import SlackWebClient


__all__ = ['ResponderMessageProcessor']

logger = logging.getLogger(__name__)


class ResponderMessageProcessor(object):
    """
    Process the response returned by Responder
    """
    def __init__(self):
        self.sender = SlackWebClient()

    def process(self, response, channel):
        """
        Process responder's response
        """
        logger.debug("Recieved responder response: %s" % (str(response)))
        if response:
            text = response.query_result.fulfillment_text
        else:
            text = str(response) + "\nI can not perform this yet. This is coming soon!"

        return self.sender.send_text(text=text, channel=channel)
