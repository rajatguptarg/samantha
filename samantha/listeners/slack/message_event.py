#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import slack
import logging

from samantha.responder import DiagFlowClient
from samantha.brain import ResponderMessageProcessor


__all__ = ['SlackMessageEventListener']


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
responder = DiagFlowClient().get_client()
processor = ResponderMessageProcessor()


class SlackMessageEventListener(object):
    """
    When a user sends a DM, the event type will be 'message'.
    Here we'll link the message callback to the 'message' event.
    """

    @staticmethod
    @slack.RTMClient.run_on(event="message")
    def listen(**payload):
        """Display the onboarding welcome message after receiving a message
        that contains "start".
        """
        data = payload["data"]
        channel_id = data.get("channel")
        text = data.get("text")

        logger.debug("Recieved Payload: %s" % (str(payload)))

        if not data.get("subtype") == 'bot_message':
            responder_response = responder.get_response(text)
            return processor.process(responder_response, channel_id)
