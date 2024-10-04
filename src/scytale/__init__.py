#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
Scytale is a toy cryptographic tool, intended to illustrate the main techniques
used in cryptography
"""

from importlib.metadata import version

from . import cyphers
from . import tools
from .cryptobox import CryptoBox
from .tools.alphaencoder import CryptoNumber, modpow
from .tools.alphabet import char2num, num2char, get_alphabet, get_alphabet_permutation
from .tools.hashes import sha3hash
from .tools.primes import random_prime
from .tools.rng import MT19937

__all__ = [
    "CryptoBox",
    "CryptoNumber",
    "char2num",
    "cyphers",
    "num2char",
    "get_alphabet",
    "get_alphabet_permutation",
    "sha3hash",
    "MT19937",
    "random_prime",
]

__version__ = version(__package__)

del cryptobox, tools, version
