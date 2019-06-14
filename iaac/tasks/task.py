#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description:
"""

from abc import ABCMeta, abstractmethod, ABC


__all__ = ['AnsibleTask']


class AnsibleTask(ABC):
    """
    Parent class for ansible tasks

    All task must inherit this class to get full functionality
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        super(AnsibleTask, self).__init__()
        self.module = "ansible_task"
        self.listen = None
        self.notify = None
        self.when = None
        self.register = None

    @abstractmethod
    def action(self):
        """
        Returns the task action understandable by
        Ansible YAML Loader
        """
        pass

    def filter_action(self, original_action: dict):
        """
        Removes the empty and none valued keys
        """
        filtered_action = {k: v for k, v in original_action.items() if v is not None}
        original_action.clear()
        original_action.update(filtered_action)
        return original_action
