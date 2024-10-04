#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
Tools for converting messages into numbers (back and forth)
"""

from collections.abc import Iterable

from numpy import integer as npinteger
from numpy import ndarray
from numpy import vectorize

from ..tools.alphabet import char2num, num2char, get_alphabet


def unwrap(msg):
    """String unwrapper

    Removes all characters that do not belong to the alphabet from a given
    string. They are saved into `plainchrs` and their original position is
    stored through `wlen`, so that the original string can be recovered.

    :param msg: String
    :return: Triplet with new string, lengths of the components, and
             characters splitting the components
    """
    wlen = []
    plainchrs = ""
    msg0 = ""
    count = 0
    for c in msg:
        if c in get_alphabet():
            count += 1
            msg0 += c
        else:
            wlen.append(count)
            count = 0
            plainchrs += c
    wlen.append(count)
    msg0 += (16 - len(msg0) % 16) % 16 * "="
    return msg0, wlen, plainchrs


def wrap(msg0, wlen, plainchrs, crop=False):
    """String wrapper

    The reciprocal function to the `unwrapper`

    :param msg0: The cleaned string, with possibly extra ghost characters
                 the end
    :param wlen: Length of the components
    :param plainchrs: Component-splitting non-alphabetical characters
    :param crop: Whether to crop the possible extra-characters
    """
    msg = ""
    head = 0
    for l, c in zip(wlen[:-1], plainchrs):
        msg += msg0[head : head + l]
        msg += c
        head += l
    if crop:
        msg += msg0[head : head + wlen[-1]]
    else:
        msg += msg0[head:]
    return msg


def encode_unwrapped(msg0, hexa=False):
    """Encodes an alphabetical string into numbers

    Two possible encodings: either single letter to single number,
    and the number is in the range 0:len(alphabet), or with `hexa = True`
    encoding of 16 characters into 3 32-bit numbers.

    The sequence is padded at the end with repetitions of`alphabet[0]`,
    if necessary.

    Note: the 3 numbers in the hex-encoding are still represented by
          64-bit integers, in order to (temporarily) allow for overflows.
    """
    code = []
    if hexa:
        n = 0
        j = 0
        for i in range(len(msg0) // 16):
            word = msg0[i * 16 : (i + 1) * 16]
            for c in word:
                p = char2num(c)
                for k in range(3):
                    n += (p >> 2 * k & 3) * 4**j
                    j += 1
                    if j >= 16:
                        code.append(n)
                        n = 0
                        j = 0
    else:
        for c in msg0:
            code.append(char2num(c))
    return code


def decode_to_unwrapped(code, hexa=False):
    """Reciprocal function to `encode_unwrapped`

    Turns a number-coded message into the original alphabet-message

    :param code: The encoded message
    :param hexa: Type of coding (see `encode_unwrapped`)
    :return: Original message
    """
    msg0 = ""
    if hexa:
        n = 0
        j = 0
        for c in code:
            for k in range(16):
                n += (c >> 2 * k & 3) * 4**j
                j += 1
                if j >= 3:
                    msg0 += num2char(n)
                    n = 0
                    j = 0
    else:
        for n in code:
            msg0 += num2char(n)
    return msg0


def encode_wrapped(msg, hexa=False):
    """Encodes a general message string into numbers

    Two possible encodings: either single letter to single number,
    and the number is in the range 0:len(alphabet), or with `hexa = True`
    encoding of 16 characters into 3 32-bit numbers.

    All characters that do not belong to the alphabet from a given
    string are saved into `plainchrs` and their original position is
    stored through `wlen`, so that the original string can be recovered.

    Note: the 3 numbers in the hex-encoding are still represented by
          64-bit integers, in order to (temporarily) allow for overflows.

    :param msg: String to encode
    :return: Triplet with new string, lengths of the components, and
             characters splitting the components
    """
    msg0, wlen, plainchrs = unwrap(msg)
    code = encode_unwrapped(msg0, hexa)
    return code, wlen, plainchrs


def decode_and_wrap(code, wlen, plainchrs, hexa=False, crop=False):
    """Reciprocal function to `encode_wrapped`

    :param code: The encoded message
    :param wlen: Length of the components
    :param plainchrs: Component-splitting non-alphabetical characters
    """
    msg0 = decode_to_unwrapped(code, hexa)
    msg = wrap(msg0, wlen, plainchrs, crop)
    return msg


class CryptoNumber(ndarray):
    """CryptoNumber class

    A number represented with this class has a one-to-one corresponding string

    Those numbers are internally represented by a list of integers, and the
    length of the list must be a multiple of 3.

    If `fill` is specified, the input list is padded with integers with value
    `fill` in order to attain a multiple length of 3.

    Examples
    --------

    >>> cn = CryptoNumber("E====X=====A====M=====P====L====E")
    CryptoNumber([  5,   6,   4,  13, 256,  48,   5,   0,   0])

    >> 2*cn
    CryptoNumber([ 10,  12,   8,  26, 512,  96,  10,   0,   0])

    >> cn2 = CryptoNumber([ 10,  12,   8,  26, 512,  96,  10,   0,   0])
    CryptoNumber([ 10,  12,   8,  26, 512,  96,  10,   0,   0])

    >> print(cn)
    E====X=====A====M=====P====L====E

    We can further generate a "cleaned key" from a CryptoNumber:

    >> print(cn.key())
    EXAMPLE

    It is also possible to perform floating point operations with a
    CryptoNumber:

    >> half_cn = cn/2
    >> half_cn
    CryptoNumber([  2.5,   3. ,   2. ,   6.5, 128. ,  24. ,   2.5,   0. ,
    0. ])

    However, such number does not have anymore a string representation. It can
    still be fixed by rounding each number:

    >> half_cn.fix()
    CryptoNumber([  2,   3,   2,   6, 128,  24,   2,   0,   0])

    >> print(half_cn)
    B====L====f=====F=====H====F====B
    """

    def __new__(subtype, *l, fill=None):
        if len(l) == 1:
            if isinstance(l[0], str):
                code, _, _ = encode_wrapped(l[0], True)
                obj = super().__new__(
                    subtype,
                    shape=(len(code),),
                    dtype=int,
                    buffer=None,
                    offset=0,
                    strides=None,
                    order=None,
                )
                return obj
            elif isinstance(l[0], Iterable):
                l = l[0]
        try:
            assert len(l) % 3 == 0 or not fill is None
        except AssertionError:
            raise ValueError("Crypto numbers should come in triplets of integers!")
        try:
            for e in l:
                assert isinstance(e, (int, npinteger))
        except AssertionError:
            raise ValueError("Crypto numbers should be triplets of integers!")
        if not fill is None and len(l) % 3:
            llen = len(l) + 3 - len(l) % 3
        else:
            llen = len(l)
        obj = super().__new__(
            subtype,
            shape=(llen,),
            dtype=int,
            buffer=None,
            offset=0,
            strides=None,
            order=None,
        )
        return obj

    def __init__(self, *l, fill=None):
        super().__init__()
        if len(l) == 1:
            if isinstance(l[0], str):
                l, _, _ = encode_wrapped(l[0], True)
            elif isinstance(l[0], Iterable):
                l = l[0]
        if not fill is None and len(l) % 3:
            l = list(l)
            l.extend((3 - len(l) % 3) * [fill])
        for i, e in enumerate(l):
            self[i] = e

    def __array_finalize__(self, obj):
        if obj is None:
            return

    def __str__(self):
        return decode_to_unwrapped(self, hexa=True).strip(get_alphabet()[0])

    def key(self):
        """Returns a key based on the CryptoNumber

        Note: this operation is not injective (it is not a one-to-one map)
        """
        return type(self)(self.fix().__str__().replace(get_alphabet()[0], ""))

    def fix(self):
        """Fix a CryptoNumber

        Rounds a floating-point based CryptoNumber and converts it to an integer
        CryptoNumber
        """
        return self.round().astype(int)


@vectorize
def modpow(base, exp, mod=None):
    return pow(int(base), int(exp), mod if mod is None else int(mod))
