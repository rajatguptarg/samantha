#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

from iaac.tasks.task import AnsibleTask


__all__ = ['Command']


class Command(AnsibleTask):
    """
    Ansible command task
    """
    def __init__(self, argv: list, chdir=None, creates=None, removes=None,
            warn=True, register=None, notify=None, listen=None, when=None):
        super(Command, self).__init__()
        self.module = 'command'
        self.argv = argv
        self.chdir = chdir
        self.creates = creates
        self.removes = removes
        self.warn = warn
        self.register = register
        self.notify = notify
        self.listen = listen
        self.when = when

    def action(self):
        """
        Returns the task action understandable by
        Ansible YAML Loader
        """
        original_action = dict(
            action=dict(module=self.module, args=dict(
                argv=self.argv, chdir=self.chdir, creates=self.creates,
                removes=self.removes)),
            register=self.register,
            when=self.when, notify=self.notify, listen=self.listen
        )
        return self.filter_action(original_action)
