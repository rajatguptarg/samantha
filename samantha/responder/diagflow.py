#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""


import os
import logging
import dialogflow_v2 as dialogflow
from google.oauth2 import service_account


__all__ = ['DiagFlowClient']


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DiagFlowClient(object):
    """
    API Client for Dialogue Flow
    """

    def __init__(self):
        self.project_id = os.getenv('DIAG_FLOW_PROJECT_ID', 'dev')
        self.session_id = os.getenv('DIAG_FLOW_SESSION_ID', 'dev')
        self.language_code = os.getenv('DIAG_FLOW_LANG_CODE', 'dev')
        self.credentials = None
        self.session = None
        self.session_client = None

    def get_client(self):
        """
        Returns the session client
        """
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                    os.getenv('DIAG_FLOW_CREDENTIALS_FILE', 'dev_credentials.json'))
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
