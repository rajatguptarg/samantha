#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import os
from slack import WebClient


__all__ = ['SlackWebClient']


class SlackWebClient(object):
    """
    Web client for uploading data to slack
    """
    def __init__(self):
        self._token = os.getenv('SLACK_BOT_TOKEN')
        self._client = WebClient(token=self.token, run_async=True)
