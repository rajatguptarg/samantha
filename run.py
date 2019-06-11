#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import os
import logging
import slack
import ssl as ssl_lib
import certifi
import asyncio

from samantha.listeners import SlackMessageEventListener


# ========= Event Listeners =============
message_listener = SlackMessageEventListener.listen


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context, loop=loop)
    loop.run_until_complete(rtm_client.start())
