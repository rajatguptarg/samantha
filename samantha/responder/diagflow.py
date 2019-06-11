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
    session = None
    session_client = None

    def __init__(self):
        self.project_id = os.getenv('DIAG_FLOW_PROJECT_ID')
        self.session_id = os.getenv('DIAG_FLOW_SESSION_ID')
        self.language_code = os.getenv('DIAG_FLOW_LANG_CODE')
        self.credentials = service_account.Credentials.from_service_account_file(
                os.getenv('DIAG_FLOW_CREDENTIALS_FILE'))

    def get_client(self):
        """
        Returns the session client
        """
        self.session_client = dialogflow.SessionsClient(credentials=self.credentials)
        self.session = self.session_client.session_path(self.project_id, self.session_id)
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
        except:
            return "I am unable to process this request at this moment."

        logger.debug("Dialogue Flow Response: %s", str(response))

        if response.query_result.fulfillment_text:
            return response.query_result.fulfillment_text
        else:
            return str(response) + "\nI can not perform this yet. This is coming soon!"
