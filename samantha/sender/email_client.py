#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# flake8: noqa

"""
Author: Rajat Gupta
Description:
"""

import smtplib
import logging
import email.utils
from samantha import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


__all__ = ['EmailClient']

logger = logging.getLogger(__name__)


class EmailClient(object):
    """
    SMTP Client to send emails
    """
    def __init__(self):
        super(EmailClient, self).__init__()
        smtp_config = config.get_smtp_config()
        self.username = smtp_config.username
        self.password = smtp_config.password
        self.sender = smtp_config.sender
        self.sender_name = smtp_config.sender_name
        self.host = smtp_config.host
        self.port = smtp_config.port

    def _login(self):
        """
        Login mechanism for SMTP Server
        """
        self.server = smtplib.SMTP(self.host, self.port)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.username, self.password)

    def build_email(self, recipient, subject, text, html=None, file_content=None, filename=None):
        """
        Build email body
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email.utils.formataddr((self.sender_name, self.sender))
        msg['To'] = recipient
        part1 = MIMEText(text, 'plain')
        msg.attach(part1)
        if html:
            part2 =  MIMEText(html, 'html')
            msg.attach(part2)
        if file_content and filename:
            filename = filename
            attachment = MIMEText(file_content)
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(attachment)
        logger.debug("Build email message: %s" % (msg.as_string()))
        return msg

    def send(self, recipient, message):
        """
        Send the email to recipient
        """
        try:
            self._login()
            response = self.server.sendmail(self.sender, recipient, message.as_string())
            logger.info("Send email to %s with response %s" % (recipient, str(response)))
            self.server.close()
        except Exception as e:
            logger.error("Error while sending email: %s" % (e))
