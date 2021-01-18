#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import slack
import logging

from samantha import entities
from samantha.responder import DiagFlowClient
from samantha.brain import ResponderMessageProcessor


__all__ = ['SlackMessageEventListener']


logger = logging.getLogger(__name__)
responder = DiagFlowClient().get_client()
processor = ResponderMessageProcessor()


class SlackMessageEventListener(object):
    """
    When a user sends a DM, the event type will be 'message'.
    Here we'll link the message callback to the 'message' event.
    """

    @staticmethod
    @slack.RTMClient.run_on(event="message")
    async def listen(**payload):
        """Display the onboarding welcome message after receiving a message
        that contains "start".
        """
        BLACKLIST_CHANNELS = ['C01JG2PQ75J']
        WHITELIST_CHANNELS = ['D01HVBTPU23']
        BOT_USER_ID = 'U01JAB70GAF'

        data = payload["data"]
        if not data.get("subtype") == 'bot_message':
            channel_id = data.get("channel")
            text = data.get("text")
            if (BOT_USER_ID in text) or (channel_id in WHITELIST_CHANNELS):
                user_id = data.get("user")
                user_dict = await SlackMessageEventListener.get_user(
                        user_id, payload['web_client'])
                user = entities.dict_to_object(user_dict).user
                logger.info("Recieved Payload: %s" % (str(payload)))

                responder_response = responder.get_response(text)
                if responder_response is not None:
                    return processor.process(responder_response, channel_id, user)

    @staticmethod
    async def get_user(user_id, client):
        response = await client.users_info(user=user_id)
        return response.data
