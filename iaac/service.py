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
    def __init__(self, sources: str, hosts: str, tasks: list, callback=None):
        super(AnsibleService, self).__init__()
        self._sources = sources
        self._hosts = hosts
        self._passwords = dict(vault_pass='secret')
        self._tasks = tasks
        self._callback = callback

    def initialize(self):
        """
        Setup the parameters to run ansible
        """
        context = self._set_context()   # noqa
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=self._sources)
        self.variable_manager = VariableManager(
                loader=self.loader, inventory=self.inventory)
        self.playbook = self._create_playbook()
        self._setup_tqm()

    def _create_playbook(self):
        """
        Create ansible playbook
        """
        self._play_source = dict(
                name='Ansible Playbook',
                hosts=self._hosts,
                gather_facts='yes',
                tasks=self._tasks
        )
        return Play().load(
                self._play_source, variable_manager=self.variable_manager,
                loader=self.loader)

    def _setup_tqm(self):
        self._tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self._passwords,
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
        context.CLIARGS = ImmutableDict(connection='ssh', forks=10, become=None,
                remote_user='rajat',
                become_method=True, become_user='root', check=False, diff=False,
                verbosity=3)
        return context
