#!/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 Flavio Calvo (UNIL / DCSR)
# All rights reserved.

"""
Tools for operating with prime numbers
"""

from itertools import compress, count

import numpy as np
from scipy.optimize import fsolve
from scipy.special import expi


maxN = 2**20


def isprime(n):
    """Checks if a number is prime

    :param n: Number
    :return: True/False
    """
    return n > 1 and all(n % i for i in range(2, int(n**0.5) + 1))


def coprime(l):
    """Find a coprime

    Propose a number that is coprime to `l`, strictly smaller than `l` but
    as close as possible, and with a Hamming weight of 1 if possible.

    :param l: Number
    :return: Coprime
    """
    for i in range(int(np.log(l - 1) / np.log(2)), 2, -1):
        e = 2**i + 1
        if np.gcd(e, l) == 1:
            return e
    for e in range(l - 1, 1, -1):
        if np.gcd(e, l) == 1:
            return e
    raise RuntimeError("No coprime found")


def primeList(rg):
    """Establish a list of prime numbers within a range

    :param rg: Range
    :return: List of primes
    """
    sieve = (isprime(i) for i in count(2))
    return list(compress(rg, sieve))


primeList.all = np.array(primeList(range(2, 1 + maxN)))
nprimes = len(primeList.all)
pmid = int(
    fsolve(
        lambda x: expi(np.log(nprimes))
        - 2 * expi(np.log(x))
        + expi(np.log(2**32 / (nprimes * np.log(nprimes)))),
        nprimes,
    ).item()
)
pmax = int((pmid / 3 + 2 * len(primeList.all)) / 3)
pmin = int(np.min(np.argwhere(primeList.all > 2**32 / primeList.all[pmax])))
primeList.bigs = primeList.all[pmax:]
primeList.smalls = primeList.all[pmin : min(pmid, pmin + len(primeList.bigs))]
