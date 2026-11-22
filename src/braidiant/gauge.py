"""Unitary basis rephasing for multiplicity-free fusion vertices."""
from __future__ import annotations
from collections.abc import Mapping
import cmath
from .model import FusionModel, ModelError


def regauge(model: FusionModel, phases: Mapping[tuple[str, str, str], complex],
            *, name: str | None = None) -> FusionModel:
    """Rephase fusion vertices by unimodular g[a,b,c].

    With the conventions in model.py:
      F'_{ef} = (g_ab^e g_ec^d)/(g_bc^f g_af^d) F_{ef}
      R'_{ab}^c = (g_ab^c/g_ba^c) R_{ab}^c.
    Undefined vertices default to g=1; unit vertices must have g=1.
    """
    for (a, b, c), g in phases.items():
        if c not in model.fuse(a, b):
            raise ModelError(f"phase key is not a fusion vertex: {(a,b,c)}")
        if abs(abs(g) - 1) > 1e-10:
            raise ModelError("vertex gauges must be unit modulus")
        if (a == model.unit or b == model.unit) and abs(g - 1) > 1e-10:
            raise ModelError("unit vertex gauge is fixed at 1")
    def g(a,b,c):
        return complex(phases.get((a,b,c), 1))
    F = {}
    for (a,b,c,d,e,f), value in model.f_symbols.items():
        F[a,b,c,d,e,f] = value * g(a,b,e) * g(e,c,d) / (g(b,c,f) * g(a,f,d))
    R = {}
    for (a,b,c), value in model.r_symbols.items():
        R[a,b,c] = value * g(a,b,c) / g(b,a,c)
    return FusionModel(name or f"{model.name} [regauged]", model.charges, model.unit,
                       dict(model.fusion), F, R)
