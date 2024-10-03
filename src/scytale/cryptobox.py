#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
Main cryptographic module
"""

from .tools.alphaencoder import encode_wrapped, decode_and_wrap


class CryptoBox(object):
    """CryptoBox class

    This is the main class for encrypting/decrypting messages. The messages
    are first encoded into lists of integers, and then call-back routines are
    used for encrypting does according to an implemented cypher method.

    By default, the text-to-number encoding of messages transforms each letter
    of the alphabet into its own position in the alphabet. However, if
    `encoder.hexa` is `True`, the `CryptoNumber` encoding scheme is used
    instead (this allows more complex arithmetics on 32bit integers).

    If both `encoder.hexa` and `encoder.double_count` are `True`, then encoder
    will then be able to perform full 64-bit arithmetic, and the result will
    be decoded accordingly, producing an output string twice as long.

    Usage
    -----

    For `m` a given number at position `pos` in the original messages, and `w`
    its cyphered representation with the encryption key `key`, we will define
    the following call-backs:

    >>> def encoder(m, pos, key):
    >>>     ...
    >>>     return w

    >>> def decoder(w, pos, key):
    >>>     ...
    >>>     return m

    We can then instantiate the CryptoBox:

    >>> cb = CryptoBox(encoder, decoder)

    And encrypt and decrypt messages:

    >>> cyph = cb.encrypt(msg, key)
    >>> msg = cb.decrypt(cyph, key)
    """

    def __init__(self, encoder, decoder, hexa=False, double_count=False):
        self._encoder = encoder
        self._decoder = decoder
        self._hexa = hexa
        self._double_count = double_count
        if hasattr(encoder, "hexa"):
            self._hexa = encoder.hexa
        if hasattr(encoder, "double_count"):
            self._double_count = encoder.double_count

    def encrypt(self, msg, key=None):
        """Encrypt a message

        :param msg: Plain message
        :param key: Key
        :return: Encrypted message
        """
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

    def decrypt(self, cipher_msg, key=None):
        """Decrypt a message

        :param msg: Encrypted message
        :param key: Key
        :return: Plain message
        """
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
