#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from datetime import datetime
from ansible.plugins.callback import CallbackBase
from ansible.parsing.ajson import AnsibleJSONEncoder


class CallbackModule(CallbackBase):
    """
    This callback module tells you how long your plays ran for.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'custom'

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.results = []
        self.start_time = datetime.now()

    def _days_hours_minutes_seconds(self, runtime):
        ''' internal helper method for this callback '''
        minutes = (runtime.seconds // 60) % 60
        r_seconds = runtime.seconds - (minutes * 60)
        return runtime.days, runtime.seconds // 3600, minutes, r_seconds

    def v2_runner_on_ok(self, result, **kwargs):
        """
        Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        f= open("guru99.txt","w+")
        f.close()
        host = result._host
        self.results.append({host.name: result._result})
        if result.is_changed():
            self._display.display(json.dumps({host.name: result._result}, indent=4))

    def v2_playbook_on_stats(self, stats, **kwargs):
        """
        Returns the status of the play run
        """
        end_time = datetime.now()
        runtime = end_time - self.start_time
        run_time_in_secs = runtime.seconds

        hosts = sorted(stats.processed.keys())

        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s

        custom_stats = {}
        global_custom_stats = {}

        custom_stats.update(run_time = run_time_in_secs)
        custom_stats.update(dict((self._convert_host_to_name(k), v) for k, v in stats.custom.items()))
        global_custom_stats.update(custom_stats.pop('_run', {}))

        output = {
            'plays': self.results,
            'stats': summary,
            'custom_stats': custom_stats,
            'global_custom_stats': global_custom_stats,
        }

        self._display.display(json.dumps(output, cls=AnsibleJSONEncoder, indent=4, sort_keys=True))

    def _convert_host_to_name(self, key):
        if isinstance(key, (Host,)):
            return key.get_name()
        return key
