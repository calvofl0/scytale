#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
Hash functions
"""

import hashlib

from numpy import array

from .alphaencoder import CryptoNumber


def sha3hash(msg):
    """Hash a message

    Uses the SHA3-256 algorithm in order to create a hash that is then
    converted into a CryptoNumber

    :param msg: Message
    :return: Hash
    """
    s = hashlib.sha3_256(bytes(msg, "utf8")).digest()
    return str(
        CryptoNumber(
            array([i for i in s[0::4]])
            + (array([i for i in s[1::4]]) << 8)
            + (array([i for i in s[2::4]]) << 16)
            + (array([i for i in s[3::4]]) << 24),
            fill=0,
        )
    )
