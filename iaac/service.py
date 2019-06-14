#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible import context
import ansible.constants as C


__all__ = ['AnsibleService']


class AnsibleService(object):
    """
    Ansible service class object
    """
    def __init__(self):
        super(AnsibleService, self).__init__()
        self.loader = DataLoader()
        self._password = dict(vault_pass='samantha2019')

    def setup(self, callback, sources: str, hosts, tasks: list):
        """
        Setup the parameters to run ansible
        """
        context = self._set_context()   # noqa
        self.inventory = InventoryManager(loader=self.loader, sources=sources)
        self.variable_manager = VariableManager(
                loader=self.loader, inventory=self.inventory)
        self._callback = callback
        self.playbook = self._create_playbook(hosts, tasks)
        self._setup_tqm(self._callback)

    def _create_playbook(self, hosts, tasks, name='Ansible Playbook'):
        """
        Create ansible playbook
        """
        self._play_source = dict(
                name=name,
                hosts=hosts,
                gather_facts='yes',
                tasks=tasks
        )
        return Play().load(
                self._play_source, variable_manager=self.variable_manager,
                loader=self.loader)

    def _setup_tqm(self):
        self._tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                password=self._password,
                stdout_callback=self._callback,
        )

    def run(self):
        """
        Run the ansible playbook
        """
        result = -1
        context = self._set_context()  # noqa
        try:
            result = self._tqm.run(self.playbook)
        finally:
            if self._tqm is not None:
                self._tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
        return result

    def _set_context(self):
        """
        Setup the context object
        """
        context.CLIARGS = ImmutableDict(
                connection='ssh', forks=10, verbosity=3, remote_user='rajat',
                become=True, become_method=None, become_user=None, check=False,
                diff=False)
        return context
