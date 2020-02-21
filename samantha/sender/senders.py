#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""


from samantha.sender.slack_client import SlackWebClient
from samantha.sender.email_client import EmailClient


__all__ = ['Sender']


class Sender(object):
    """
    Sender API

    Future version will include email sender.
    """
    def __init__(self):
        super(Sender, self).__init__()
        self.slack_client = SlackWebClient()
        self.email_client = EmailClient()

    def get_slack_client(self):
        return self.slack_client

    def get_email_client(self):
        return self.email_client
