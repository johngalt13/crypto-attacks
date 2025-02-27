import logging
import os
import sys

from sage.all import ZZ

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))))
if sys.path[1] != path:
    sys.path.insert(1, path)

from shared.small_roots import herrmann_may


def factorize(N, partial_p, Q, m=1, t=None):
    """
    Recovers the prime factors from a modulus if the modulus is unbalanced and bits are known.
    More information: Brier E. et al., "Factoring Unbalanced Moduli with Known Bits" (Section 4)
    :param N: the modulus: N = p * q > q ** 3
    :param partial_p: the partial prime factor p (PartialInteger)
    :param Q: the bit length of q
    :param m: the m value to use for the small roots method (default: 1)
    :param t: the t value to use for the small roots method (default: automatically computed using m)
    :return: a tuple containing the prime factors, or None if the factors could not be found
    """
    W = partial_p.get_unknown_lsb()
    assert W > 0, "Number of unknown lsb must be greater than 0 (try adding a dummy unknown bit)."
    v, L = partial_p.get_known_middle()
    assert 3 * L ** 2 + (4 * W - 6 * Q) * L + 3 * Q ** 2 - 8 * Q * W > 0, "Bound check failed."
    delta = Q / (W + L)

    x, y = ZZ["x", "y"].gens()
    a = v * 2 ** W
    f = x * (a + y) - N
    X = 2 ** Q
    Y = 2 ** W
    t = int((1 - 2 * delta) * m) if t is None else t
    logging.info(f"Trying m = {m}, t = {t}...")
    for x0, y0 in herrmann_may.modular_bivariate(f, 2 ** (W + L), m, t, X, Y):
        q = x0
        if q != 0 and N % q == 0:
            return N // q, q

    return None
