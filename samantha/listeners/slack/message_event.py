#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import slack
import logging


__all__ = ['SlackMessageEventListener']


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
        web_client = payload["web_client"]
        channel_id = data.get("channel")

        if not data.get("subtype") == 'bot_message':
            logger.debug("Recieved Payload: %s" % (str(payload)))
            return web_client.chat_postMessage(channel=channel_id, text="Hi")
