#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description: Infrastructure as a Code using Ansible
"""

from iaac.callback_plugin import ResultCallback
from iaac.service import AnsibleService
from iaac import tasks


__all__ = ['ResultCallback', 'AnsibleService']
