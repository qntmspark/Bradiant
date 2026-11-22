"""Reference numerical models with explicit documented braiding conventions."""
import cmath
import math
from .model import FusionModel, model_from_tables


def fibonacci() -> FusionModel:
    """Unitary Fibonacci category with objects 1, tau and total charge fixed per sector."""
    charges = ("1", "tau")
    fusion = {
        ("1", "1"): ("1",),
        ("1", "tau"): ("tau",),
        ("tau", "1"): ("tau",),
        ("tau", "tau"): ("1", "tau"),
    }
    phi = (1 + math.sqrt(5)) / 2
    overrides = {}
    for i, e in enumerate(("1", "tau")):
        for j, f in enumerate(("1", "tau")):
            v = ((1 / phi, phi ** -0.5), (phi ** -0.5, -1 / phi))[i][j]
            overrides["tau", "tau", "tau", "tau", e, f] = v
    r = {}
    for a in charges:
        for b in charges:
            for c in fusion[a, b]:
                r[a, b, c] = 1 + 0j
    r["tau", "tau", "1"] = cmath.exp(-4j * math.pi / 5)
    r["tau", "tau", "tau"] = cmath.exp(3j * math.pi / 5)
    return model_from_tables("Fibonacci", charges, "1", fusion, overrides, r)


def cyclic(n: int = 3, k: int = 1) -> FusionModel:
    """Pointed Z_n category with trivial associator and bicharacter exp(2πikab/n).

    It is not claimed to be a modular category for every (n,k).
    """
    if n < 2 or n > 64:
        raise ValueError("n must be between 2 and 64")
    charges = tuple(str(i) for i in range(n))
    fusion = {(str(a), str(b)): (str((a + b) % n),)
              for a in range(n) for b in range(n)}
    r = {(str(a), str(b), str((a + b) % n)): cmath.exp(2j * math.pi * k * a * b / n)
         for a in range(n) for b in range(n)}
    return model_from_tables(f"Z{n}(k={k})", charges, "0", fusion, {}, r)


def ising() -> FusionModel:
    """Chiral Ising data: 1, psi (fermion), sigma (non-Abelian charge).

    Conventions: F[sigma,sigma,sigma;sigma] is the normalized Hadamard;
    the two scalar -1 associators are (sigma,psi,sigma)->psi and
    (psi,sigma,psi)->sigma. Braiding uses R_sigma,sigma^1=e^{-iπ/8}.
    """
    charges = ("1", "psi", "sigma")
    fusion = {}
    for a in charges:
        for b in charges:
            if a == "1":
                result = (b,)
            elif b == "1":
                result = (a,)
            elif a == b == "sigma":
                result = ("1", "psi")
            elif a == b == "psi":
                result = ("1",)
            else:
                result = ("sigma",)
            fusion[a, b] = result
    overrides = {}
    for i, e in enumerate(("1", "psi")):
        for j, f in enumerate(("1", "psi")):
            overrides["sigma", "sigma", "sigma", "sigma", e, f] = (
                -1 if (i, j) == (1, 1) else 1) / math.sqrt(2)
    overrides["sigma", "psi", "sigma", "psi", "sigma", "sigma"] = -1
    overrides["psi", "sigma", "psi", "sigma", "sigma", "sigma"] = -1
    r = {(a, b, c): 1 + 0j for (a, b), targets in fusion.items() for c in targets}
    r["sigma", "sigma", "1"] = cmath.exp(-1j * math.pi / 8)
    r["sigma", "sigma", "psi"] = cmath.exp(3j * math.pi / 8)
    r["sigma", "psi", "sigma"] = -1j
    r["psi", "sigma", "sigma"] = -1j
    r["psi", "psi", "1"] = -1
    return model_from_tables("Ising", charges, "1", fusion, overrides, r)
