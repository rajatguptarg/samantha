#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

from iaac.tasks.task import AnsibleTask


__all__ = ['Debug']


class Debug(AnsibleTask):
    """
    Ansible debug task

    When called without any params, default print Hello World
    """
    def __init__(self, msg='Hello world!', var=None, verbosity=0,
            warn=True, register=None, notify=None, listen=None, when=None):
        super(Debug, self).__init__()
        self.module = 'debug'
        self.msg = msg
        self.var = var
        self.verbosity = verbosity
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
                msg=self.msg, var=self.var, verbosity=self.verbosity)),
            register=self.register,
            when=self.when, notify=self.notify, listen=self.listen
        )
        return self.filter_action(original_action)
