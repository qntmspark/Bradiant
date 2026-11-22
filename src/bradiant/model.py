"""Finite unitary, multiplicity-free braided fusion data.

Conventions: F[a,b,c,d][e,f] maps the basis path ((ab)_e c)_d
into (a (bc)_f)_d, and R[a,b,c] is the exchange amplitude a,b -> b,a
in the fusion channel c. All quantities are numerical complex values.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping
import numpy as np


class ModelError(ValueError):
    """Invalid fusion input or incoherent declared shape."""


@dataclass(frozen=True)
class FusionModel:
    name: str
    charges: tuple[str, ...]
    unit: str
    fusion: Mapping[tuple[str, str], tuple[str, ...]]
    f_symbols: Mapping[tuple[str, str, str, str, str, str], complex]
    r_symbols: Mapping[tuple[str, str, str], complex]

    def __post_init__(self) -> None:
        if (not self.charges or any(not isinstance(a, str) or not a for a in self.charges)
                or len(set(self.charges)) != len(self.charges)):
            raise ModelError("charges must be nonempty and distinct")
        if self.unit not in self.charges:
            raise ModelError("unit is not a charge")
        names = set(self.charges)
        expected_fusion = {(a, b) for a in self.charges for b in self.charges}
        if set(self.fusion) != expected_fusion:
            raise ModelError("fusion table has missing or unexpected entries")
        expected_r = set()
        expected_f = set()
        for a in self.charges:
            for b in self.charges:
                outputs = self.fusion.get((a, b))
                if outputs is None or len(outputs) != len(set(outputs)) or any(x not in names for x in outputs):
                    raise ModelError(f"missing/invalid fusion channel: {(a, b)}")
                if a == self.unit and outputs != (b,):
                    raise ModelError("unit must fuse trivially on the left")
                if b == self.unit and outputs != (a,):
                    raise ModelError("unit must fuse trivially on the right")
                if set(outputs) != set(self.fusion.get((b, a), ())):
                    raise ModelError("braided fusion must be commutative")
                if not outputs:
                    raise ModelError(f"empty fusion product: {(a, b)}")
                for c in outputs:
                    expected_r.add((a, b, c))
                    if (a, b, c) not in self.r_symbols:
                        raise ModelError(f"R symbol missing for {(a,b,c)}")
        for a in self.charges:
            candidates = [b for b in self.charges if self.unit in self.fusion[a, b]]
            if len(candidates) != 1:
                raise ModelError(f"simple object {a} must have a unique dual")
        if set(self.r_symbols) != expected_r:
            raise ModelError("R table has unexpected entries")
        for entry, value in list(self.f_symbols.items()) + list(self.r_symbols.items()):
            z = complex(value)
            if not isfinite(z.real) or not isfinite(z.imag):
                raise ModelError(f"nonfinite symbol at {entry}")
        for a in self.charges:
            for b in self.charges:
                for c in self.charges:
                    for d in self.charges:
                        left, right = self.channels(a, b, c, d)
                        if len(left) != len(right):
                            raise ModelError(f"fusion not associative: {(a,b,c,d)}")
                        for e in left:
                            for f in right:
                                expected_f.add((a, b, c, d, e, f))
                                if (a, b, c, d, e, f) not in self.f_symbols:
                                    raise ModelError(f"F symbol missing for {(a,b,c,d,e,f)}")
        if set(self.f_symbols) != expected_f:
            raise ModelError("F table has unexpected entries")

    def dual(self, a: str) -> str:
        """Unique simple dual as determined by the vacuum fusion channel."""
        if a not in self.charges:
            raise ModelError(f"unknown charge: {a}")
        return next(b for b in self.charges if self.unit in self.fuse(a, b))

    def fuse(self, a: str, b: str) -> tuple[str, ...]:
        return self.fusion[(a, b)]

    def channels(self, a: str, b: str, c: str, d: str) -> tuple[list[str], list[str]]:
        left = [e for e in self.fuse(a, b) if d in self.fuse(e, c)]
        right = [f for f in self.fuse(b, c) if d in self.fuse(a, f)]
        return left, right

    def F(self, a: str, b: str, c: str, d: str, e: str, f: str) -> complex:
        return self.f_symbols[(a, b, c, d, e, f)]

    def R(self, a: str, b: str, c: str) -> complex:
        return self.r_symbols[(a, b, c)]

    def f_matrix(self, a: str, b: str, c: str, d: str) -> np.ndarray:
        left, right = self.channels(a, b, c, d)
        return np.array([[self.F(a, b, c, d, e, f) for f in right] for e in left], dtype=complex)


def model_from_tables(name: str, charges: tuple[str, ...], unit: str,
                      fusion: Mapping[tuple[str, str], tuple[str, ...]],
                      f_overrides: Mapping[tuple[str, str, str, str, str, str], complex] | None = None,
                      r_symbols: Mapping[tuple[str, str, str], complex] | None = None) -> FusionModel:
    """Build from explicit F exceptions. Default F is the identity ONLY when valid.

    Use this shortcut only for sparse models known to have trivial 1x1
    associators; general models should construct FusionModel with all entries.
    """
    overrides = f_overrides or {}
    if r_symbols is None:
        raise ModelError("R data must be supplied")
    fs: dict[tuple[str, str, str, str, str, str], complex] = {}
    for a in charges:
        for b in charges:
            for c in charges:
                for d in charges:
                    left = [e for e in fusion[a, b] if d in fusion[e, c]]
                    right = [f for f in fusion[b, c] if d in fusion[a, f]]
                    for i, e in enumerate(left):
                        for j, f in enumerate(right):
                            key = a, b, c, d, e, f
                            fs[key] = complex(overrides.get(key, float(i == j)))
    unknown_overrides = set(overrides).difference(fs)
    if unknown_overrides:
        raise ModelError(f"F override refers to a nonexistent channel: {sorted(unknown_overrides)!r}")
    return FusionModel(name, charges, unit, fusion, fs, r_symbols)
