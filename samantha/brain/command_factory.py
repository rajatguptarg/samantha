#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

from samantha.brain.commands import MPStat
from samantha.brain.commands import Welcome


__all__ = ['CommandFactory']


class CommandFactory(object):
    """
    Returns the command object for different actions
    """
    def __init__(self):
        """
        Command map includes the command and dialogflow action mapping

        To add new or more commands, add dialogflow action as a key and
        map to the bot's command object
        """
        self.command_map = {
            'mpstat': self._prepare_mpstat_command,
        }
        self.default_command = self._prepare_welcome_command
        super(CommandFactory, self).__init__()

    def get_command(self, response, channel, user):
        """
        Takes an action and returns the command, if action doesnt
        have command, returns the welcome command
        """
        action = response.query_result.action
        return self.command_map.get(action, self.default_command)(response, channel, user)

    def _prepare_welcome_command(self, response, channel, user):
        """
        Returns the prepared welcome message command
        """
        return Welcome(response, channel, user)

    def _prepare_mpstat_command(self, response, channel, user):
        """
        Returns the prepared log fetch command
        """
        return MPStat(response, channel, user)
