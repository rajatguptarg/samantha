#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# flake8: noqa

"""
Author: Rajat Gupta
Description:
"""

import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


__all__ = ['EmailClient']


class EmailClient(object):
    """
    SMTP Client to send emails
    """
    def __init__(self, username, password, host, port=587):
        super(EmailClient, self).__init__()
        self.username = username
        self.password = password
        self.sender = 'samantha@entelios.com'
        self.sender_name = 'Samantha Alerts'
        self.host = host
        self.port = port

    def _login(self):
        """
        Login mechanism for SMTP Server
        """
        pass

    def build_email(self, subject, text, html, file_content, filename):
        """
        Build email body
        """
        pass

    def send(self, to, message):
        """
        Send the email to recipient
        """
        pass
