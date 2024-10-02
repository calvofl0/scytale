#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
Implementation of the well-known RSA cipher mechanism
"""


from ..tools.rng import MT19937


_rng = MT19937()


def genRSAkeys(rng=_rng):
    from numpy import lcm
    from ..tools.alphaencoder import CryptoNumber
    from ..tools.primes import coprime, primeList

    p = rng.choice(primeList.smalls)
    q = rng.choice(primeList.bigs)
    n = p * q
    l = int(lcm(p - 1, q - 1))
    e = coprime(l)
    d = pow(e, -1, l)
    return str(
        CryptoNumber([e & 2**32 - 1, e >> 32, n & 2**32 - 1, n >> 32], fill=0)
    ), str(CryptoNumber([d & 2**32 - 1, d >> 32, n & 2**32 - 1, n >> 32], fill=0))


def RSA_coder(m, pos, key):
    from ..tools.alphaencoder import CryptoNumber

    b0, b1, n0, n1, _, _ = CryptoNumber(key)
    b = int(b0 + (b1 << 32))
    n = int(n0 + (n1 << 32))
    return pow(m, b, n)


RSA_coder.hexa = True
RSA_coder.double_count = True

encoder = RSA_coder
decoder = RSA_coder

del MT19937, RSA_coder, _rng
