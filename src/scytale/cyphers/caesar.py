#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
A generalization of the Caesar cipher, allowing for a variable shift
depending on a given position and key
"""


def _shift(pos, key):
    from ..tools.alphabet import char2num

    return char2num(key[pos % len(key)])


def encoder(n, pos, key):
    from ..tools.alphabet import get_alphabet

    shift = _shift(pos, key)
    return (n + shift) % len(get_alphabet())


def decoder(n, pos, key):
    from ..tools.alphabet import get_alphabet

    shift = _shift(pos, key)
    return (n - shift) % len(get_alphabet())
