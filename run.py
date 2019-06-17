#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import logging
import slack
import ssl as ssl_lib
import certifi
import asyncio
import configargparse
from pyfiglet import Figlet

from samantha.__project_name__ import __project_name__
from samantha.__version__ import __version__

from samantha.listeners import SlackMessageEventListener


# ========= Event Listeners =============
message_listener = SlackMessageEventListener.listen


def main():
    """
    Start App Function
    """
    parser = configargparse.ArgParser(description='Samatha Configurations')

    parser.add_argument(
        '-t', '--slack-bot-token', dest='slack_bot_token', env_var='SLACK_BOT_TOKEN',
        help='Slack bot token in format of xoxb-xx-xx'
    )
    parser.add_argument(
        '-p', '--dialogflow-project-id', dest='dialogflow_project_id',
        env_var='DIAG_FLOW_PROJECT_ID', help='Project of DiaglogFlow Project'
    )
    parser.add_argument(
        '-s', '--dialogflow-session-id', dest='dialogflow_session_id',
        env_var='DIAG_FLOW_SESSION_ID', help='Session of DiaglogFlow'
    )
    parser.add_argument(
        '-lc', '--dialogflow-lang-code', dest='dialogflow_lang_code',
        env_var='DIAG_FLOW_LANG_CODE', help='Language code for DiaglogFlow'
    )
    parser.add_argument(
        '-c', '--dialogflow-credentials-file', dest='dialogflow_credentials_file',
        env_var='DIAG_FLOW_CREDENTIALS_FILE', help='Credentials for DiaglogFlow Project'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        env_var='LOG_LEVEL', help='Enable debug logging'
    )
    parser.add_argument(
        '-ap', '--ansible-vault-pass', dest='ansible_vault_pass',
        env_var='ANSIBLE_VAULT_PASS', help='Ansible vault password'
    )
    parser.add_argument(
        '-i', '--ansible-inventory-file', dest='ansible_inventory_file',
        env_var='ANSIBLE_INVENTORY_FILE', help='Path for ansible inventory files'
    )

    args = parser.parse_args()

    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    f = Figlet(font='larry3d')

    # Logger Configurations
    logger = logging.getLogger()
    logger.setLevel(loglevel)
    logger.addHandler(logging.StreamHandler())

    # Application configuration
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = args.slack_bot_token
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    rtm_client = slack.RTMClient(
            token=slack_token, ssl=ssl_context, loop=loop, run_async=True,
            auto_reconnect=True)
    print(f.renderText('{} {}'.format(__project_name__, __version__)))
    loop.run_until_complete(rtm_client.start())


if __name__ == '__main__':
    main()
