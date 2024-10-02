#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.


"""
All tools related to the alphabet
"""


from .rng import MT19937


_alphabet = (
    "="
    + "".join(chr(i) for i in range(ord("A"), 1 + ord("Z")))
    + "".join(chr(i) for i in range(ord("a"), 1 + ord("z")))
    + "+-%&/()!#@£"
)


def _permuted_alphabet():
    rng = MT19937()
    return "".join(rng.permutation([c for c in _alphabet]))


_permuted_alphabet = _permuted_alphabet()


def get_alphabet():
    return _alphabet


def char2num(c):
    return _alphabet.find(c)


def num2char(n):
    return _alphabet[n]


def code_divide(code, n, base=len(get_alphabet())):
    for i in range(len(code) - 1, 0, -1):
        code[i - 1] += (code[i] % n) * base
        code[i] //= n
    r = code[0] % n
    code[0] //= n
    return r


def get_alphabet_permutation(key):
    alphalen = len(get_alphabet())
    step = max(1, alphalen // len(key))
    coded_key = [char2num(c) for c in key]
    key_code = [char2num(c) for c in _permuted_alphabet]
    for i, n in enumerate(coded_key):
        pos = i * step % alphalen
        key_code[pos] = (key_code[pos] + n) % alphalen
    i = 2
    permutation = []
    for i in range(2, 1 + len(get_alphabet())):
        permutation.append(code_divide(key_code, i))
    permutation.reverse()
    permuted_alphabet_code = []
    alphabet = [char2num(c) for c in get_alphabet()]
    for i in permutation:
        permuted_alphabet_code.append(alphabet.pop(i))
    permuted_alphabet_code.append(alphabet.pop(0))

    return "".join([num2char(n) for n in permuted_alphabet_code])
