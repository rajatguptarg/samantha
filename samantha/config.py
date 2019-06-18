#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import configargparse
from pathlib import Path
from ruamel.yaml import YAML
from collections import namedtuple


def build_config():
    """
    Build the config file
    """
    parser = configargparse.get_argument_parser()
    parser.add_argument(
        '-c', '--config_file', dest='config_file', env_var='CONFIG_FILE',
        default='config.yml',
        help='Configuration file for the application'
    )
    opts = parser.parse_known_args()[0]
    path = Path(opts.config_file)

    yaml = YAML(typ='safe')
    return yaml.load(path)


def get_smtp_config():
    """
    Returns smtp client configs
    """
    app_config = build_config()
    smtp_config = app_config['smtp']
    SMTPConfig = namedtuple('SMTPConfig', sorted(smtp_config))
    return SMTPConfig(**smtp_config)


def get_ansible_config():
    """
    Returns ansible config
    """
    app_config = build_config()
    config = app_config['ansible']
    AnsibleConfig = namedtuple('AnsibleConfig', sorted(config))
    return AnsibleConfig(**config)


def get_dialogflow_config():
    """
    Returns dialog flow config
    """
    app_config = build_config()
    config = app_config['dialogflow']
    DialogFlowConfig = namedtuple('DialogFlowConfig', sorted(config))
    return DialogFlowConfig(**config)


def get_slack_config():
    """
    Returns the slack config
    """
    app_config = build_config()
    config = app_config['slack']
    SlackConfig = namedtuple('SlackConfig', sorted(config))
    return SlackConfig(**config)


def get_log_file_map():
    """
    Returns the log file dict
    """
    app_config = build_config()
    config = app_config['log_file_map']
    return config
