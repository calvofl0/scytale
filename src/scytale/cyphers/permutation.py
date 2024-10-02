#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
A permutation cipher

A map key->permutation allows to build a permutation cipher out
of a provided key
"""


def encoder(n, pos, key):
    from ..tools.alphabet import char2num, get_alphabet_permutation

    try:
        permutation = encoder.permutations[key]
    except KeyError:
        new_alphabet = get_alphabet_permutation(key)
        permutation = [char2num(c) for c in new_alphabet]
        encoder.permutations[key] = permutation
    return permutation[n]


encoder.permutations = {}


def decoder(n, pos, key):
    from ..tools.alphabet import char2num, get_alphabet_permutation

    try:
        permutation = decoder.permutations[key]
    except KeyError:
        new_alphabet = get_alphabet_permutation(key)
        inv_permutation = [char2num(c) for c in new_alphabet]
        permutation = len(new_alphabet) * [0]
        for i in inv_permutation:
            permutation[inv_permutation[i]] = i
    return permutation[n]


decoder.permutations = {}
