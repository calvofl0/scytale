#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
A permutation cipher

A map key->permutation allows to build a permutation cipher out
of a provided key, which can either be a new (reordered) alphabet,
or a `CryptoNumber`, in which case the key is mapped to an arbitrary
permutation of the alphabet.
"""


def encoder(n, pos, key):
    from ..tools.alphabet import char2num, get_alphabet_permutation
    from ..tools.alphaencoder import CryptoNumber

    if isinstance(key, CryptoNumber):
        is_cryptonumber = True
    else:
        is_cryptonumber = False
    try:
        if is_cryptonumber:
            permutation = encoder.permutations[tuple(key)]
        else:
            permutation = encoder.permutations[key]
    except KeyError:
        if is_cryptonumber:
            new_alphabet = get_alphabet_permutation(str(key))
            key = tuple(key)
        elif key is None:
            new_alphabet = get_alphabet_permutation()
        else:
            new_alphabet = key
        permutation = [char2num(c) for c in new_alphabet]
        encoder.permutations[key] = permutation
    return permutation[n]


encoder.permutations = {}


def decoder(n, pos, key):
    from ..tools.alphabet import char2num, get_alphabet_permutation
    from ..tools.alphaencoder import CryptoNumber

    if isinstance(key, CryptoNumber):
        is_cryptonumber = True
    else:
        is_cryptonumber = False
    try:
        if is_cryptonumber:
            permutation = decoder.permutations[tuple(key)]
        else:
            permutation = decoder.permutations[key]
    except KeyError:
        if is_cryptonumber:
            new_alphabet = get_alphabet_permutation(str(key))
            key = tuple(key)
        elif key is None:
            new_alphabet = get_alphabet_permutation()
        else:
            new_alphabet = key
        inv_permutation = [char2num(c) for c in new_alphabet]
        permutation = len(new_alphabet) * [0]
        for i in inv_permutation:
            permutation[inv_permutation[i]] = i
        decoder.permutations[key] = permutation
    return permutation[n]


decoder.permutations = {}
