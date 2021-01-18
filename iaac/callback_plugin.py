#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import json
from samantha.sender import Sender
from ansible.plugins.callback import CallbackBase


__all__ = ['ResultCallback']


class ResultCallback(CallbackBase):
    """
    A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'custom_2'

    def __init__(self):
        super(ResultCallback, self).__init__()
        self.sender = Sender()

    def v2_runner_on_ok(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_skipped(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_unreachable(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_no_hosts(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        pass

    def v2_playbook_item_on_ok(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        pass

    def v2_playbook_item_on_skipped(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        pass

    def v2_playbook_on_stats(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        pass
