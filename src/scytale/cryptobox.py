#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
Main cryptographic module
"""

from .tools.alphaencoder import encode_wrapped, decode_and_wrap


class CryptoBox(object):
    def __init__(self, encoder, decoder, hexa=False, double_count=False):
        self._encoder = encoder
        self._decoder = decoder
        self._hexa = hexa
        self._double_count = double_count
        if hasattr(encoder, "hexa"):
            self._hexa = encoder.hexa
        if hasattr(encoder, "double_count"):
            self._double_count = encoder.double_count

    def encrypt(self, msg, key):
        code, wlen, plainchrs = encode_wrapped(msg, self._hexa)
        cipher_code = []
        for pos, n in enumerate(code):
            if self._double_count:
                m = self._encoder(n, pos, key)
                cipher_code.extend([m & 2**32 - 1, m >> 32])
            else:
                cipher_code.append(self._encoder(n, pos, key))
        cipher_msg = decode_and_wrap(
            cipher_code, wlen, plainchrs, self._hexa, crop=False
        )
        if self._hexa:
            return cipher_msg + wlen[-1] * " "
        else:
            return cipher_msg[: sum(wlen) % 16 - 16]

    def decrypt(self, cipher_msg, key):
        if self._hexa:
            npad = len(cipher_msg)
            cipher_msg = cipher_msg.strip(" ")
            npad -= len(cipher_msg)
        cipher_code, wlen, plainchrs = encode_wrapped(cipher_msg, self._hexa)
        if self._hexa:
            wlen.append(npad)
        code = []
        if self._double_count:
            for pos, n in enumerate(cipher_code):
                if pos % 2:
                    code.append(self._decoder(m + (n << 32), pos // 2, key))
                else:
                    m = n
        else:
            for pos, n in enumerate(cipher_code):
                code.append(self._decoder(n, pos, key))
        msg = decode_and_wrap(code, wlen, plainchrs, self._hexa, crop=True)
        return msg
