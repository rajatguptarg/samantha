#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""


import logging
import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

from samantha import config


__all__ = ['DiagFlowClient']


logger = logging.getLogger(__name__)


class DiagFlowClient(object):
    """
    API Client for Dialogue Flow
    """

    def __init__(self):
        self.opts = config.get_dialogflow_config()
        self.project_id = self.opts.project_id
        self.session_id = self.opts.session_id
        self.language_code = self.opts.lang_code
        try:
            self.credentials_file = self.opts.credentials_file
        except:
            self.credentials_file = 'dev_credentials.json'
        self.credentials = None
        self.session = None
        self.session_client = None

    def get_client(self):
        """
        Returns the session client
        """
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_file)
            self.session_client = dialogflow.SessionsClient(credentials=self.credentials)
            self.session = self.session_client.session_path(
                    self.project_id, self.session_id)
        except:
            logger.error("Unable to create grpc client")
        return self

    def get_response(self, text: str):
        """
        Get the response from Dialogue Flow API

        Input:

        text: str -> Text String
        """
        try:
            text_input = dialogflow.types.TextInput(
                    text=text, language_code=self.language_code
            )
            query_input = dialogflow.types.QueryInput(text=text_input)
            response = self.session_client.detect_intent(
                session=self.session, query_input=query_input)
            logger.debug("Dialogue Flow Response: %s", str(response))
            return response
        except Exception as e:
            logger.error("Unable to send to dialogflow with %s" % (e))
            return None
