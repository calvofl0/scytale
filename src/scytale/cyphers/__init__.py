#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
Scytale cypher algorithms: each of them implements at least an encoder and
a decoder
"""

from . import caesar
from . import permutation
from . import rsa


__all__ = [caesar, permutation, rsa]
