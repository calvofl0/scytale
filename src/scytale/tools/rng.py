#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
Random number generators
"""

from numpy import random


_seed = 12345


def MT19937(seed=_seed):
    bg = random.MT19937()
    bg.state = random.RandomState(seed).get_state()
    return random.Generator(bg)
