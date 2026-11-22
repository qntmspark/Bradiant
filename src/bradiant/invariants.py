"""Gauge-independent diagnostics for finite unitary braided fusion data.

This module computes Frobenius--Perron dimensions from the fusion ring and
channel-wise double braiding. Neither a pivotal structure nor a modular S
matrix is inferred from the input data.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
import numpy as np

from .model import FusionModel, ModelError


@dataclass(frozen=True)
class FusionInvariants:
    dimensions: dict[str, float]
    global_dimension: float
    total_quantum_dimension: float
    eigenvector_residual: float
    duals: dict[str, str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class BraidingInvariants:
    # An ordered list, rather than a dict with tuple keys, gives portable JSON.
    monodromies: list[dict]
    transparent_charges: list[str]
    transparency_tolerance: float

    def to_dict(self) -> dict:
        return asdict(self)


def fusion_matrices(model: FusionModel) -> dict[str, np.ndarray]:
    """N[a][b,c] = N_(ab)^c in the model's declared charge order."""
    labels = model.charges
    index = {charge: i for i, charge in enumerate(labels)}
    matrices = {}
    for a in labels:
        mat = np.zeros((len(labels), len(labels)), dtype=float)
        for b in labels:
            for c in model.fuse(a, b):
                mat[index[b], index[c]] = 1.0
        matrices[a] = mat
    return matrices


def fusion_invariants(model: FusionModel, *, tol: float = 1e-8) -> FusionInvariants:
    """Compute unique positive common eigenvector of fusion matrices.

    Normalized by d(unit)=1, yielding Frobenius--Perron dimensions. In a
    unitary fusion category these equal the categorical quantum dimensions.
    The reported maximum residual tests N_a d = d_a d for every a.
    """
    if not (math.isfinite(tol) and tol > 0):
        raise ValueError("tol must be finite and positive")
    matrices = fusion_matrices(model)
    all_fusion = sum(matrices.values())
    spectrum, vecs = np.linalg.eig(all_fusion)
    ix = int(np.argmax(spectrum.real))
    eigenvalue = spectrum[ix]
    vector = vecs[:, ix]
    if (abs(eigenvalue.imag) > tol or np.max(np.abs(vector.imag)) > tol):
        raise ModelError("fusion ring lacks a numerically real positive Perron vector")
    vector = vector.real
    unit_ix = model.charges.index(model.unit)
    if vector[unit_ix] < 0:
        vector = -vector
    if vector[unit_ix] <= 0:
        raise ModelError("unit entry of Perron vector is not positive")
    vector /= vector[unit_ix]
    if np.min(vector) < 1 - tol or not np.all(np.isfinite(vector)):
        raise ModelError("fusion ring lacks positive FP dimensions")
    dim = {a: float(vector[i]) for i, a in enumerate(model.charges)}
    residual = max(float(np.max(np.abs(matrix @ vector - dim[a] * vector)))
                   for a, matrix in matrices.items())
    if residual > tol:
        raise ModelError(f"fusion matrices do not share a PF eigenvector: {residual}")
    global_dimension = float(np.dot(vector, vector))
    return FusionInvariants(dim, global_dimension, math.sqrt(global_dimension), residual,
                            {a: model.dual(a) for a in model.charges})


def braiding_invariants(model: FusionModel, *, tol: float = 1e-10) -> BraidingInvariants:
    """R_ab^c R_ba^c for every channel, and the transparent (Mueger-central) objects.

    The double-braiding eigenvalues are unchanged by vertex-basis rephasings.
    Transparency is meaningful only once the model has passed a coherence audit.
    This function computes invariants of supplied data without implicitly
    certifying that those data define a valid braided category.
    """
    if not (math.isfinite(tol) and tol > 0):
        raise ValueError("tol must be finite and positive")
    monodromies: list[dict] = []
    transparent: list[str] = []
    for a in model.charges:
        central = True
        for b in model.charges:
            for c in model.fuse(a, b):
                value = model.R(a, b, c) * model.R(b, a, c)
                monodromies.append({"a": a, "b": b, "channel": c,
                                    "real": float(value.real), "imag": float(value.imag)})
                central &= abs(value - 1) <= tol
        if central:
            transparent.append(a)
    return BraidingInvariants(monodromies, transparent, tol)
