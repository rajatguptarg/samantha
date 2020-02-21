#!/usr/bin/env python3
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

    def filter_action(self, obj):
        """
        Removes the empty and none valued keys
        """
        if isinstance(obj, (list, tuple, set)):
            return type(obj)(self.filter_action(x) for x in obj if x is not None)
        elif isinstance(obj, dict):
            return type(obj)((self.filter_action(k), self.filter_action(v))
                for k, v in obj.items() if k is not None and v is not None)
        else:
            return obj
