"""Braid group representations on left-associated fusion-path spaces.

Scope: homogeneous external charges, unitary multiplicity-free fusion data.
No claim is made about non-unitary categories or braid compilation optimality.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import numpy as np
from .model import FusionModel
from .trees import (Tree, fusion_basis, leaf_ids, path_map, right_rotations)


def left_comb(n: int) -> Tree:
    if n < 2:
        raise ValueError("at least two anyons required")
    current: Tree = (0, 1)
    for i in range(2, n):
        current = (current, i)
    return current


def _adjacent_fused(tree: Tree, i: int) -> bool:
    if isinstance(tree, int):
        return False
    if tree == (i, i + 1):
        return True
    return _adjacent_fused(tree[0], i) or _adjacent_fused(tree[1], i)


def _rotation_path(start: Tree, i: int) -> list[Tree]:
    todo = deque([start])
    parent: dict[Tree, Tree | None] = {start: None}
    while todo:
        u = todo.popleft()
        if _adjacent_fused(u, i):
            path = [u]
            while parent[path[-1]] is not None:
                path.append(parent[path[-1]])
            return list(reversed(path))
        for v in right_rotations(u):
            if v not in parent:
                parent[v] = u
                todo.append(v)
    raise RuntimeError("unreachable adjacent fusion tree")


@dataclass
class BraidRepresentation:
    """Unitary matrices for sigma_i on n identical anyons in one total sector."""
    model: FusionModel
    charge: str
    number: int
    total: str

    def __post_init__(self):
        if self.number < 2 or self.number > 9:
            raise ValueError("supported number of anyons is 2..9 (exponential basis)")
        if self.charge not in self.model.charges or self.total not in self.model.charges:
            raise ValueError("unknown charge")
        self.labels = (self.charge,) * self.number
        self.tree = left_comb(self.number)
        self.basis = fusion_basis(self.model, self.tree, self.labels, self.total)
        if not self.basis:
            raise ValueError("no fusion paths in the requested total-charge sector")
        self._generators: dict[int, np.ndarray] = {}

    @property
    def dimension(self) -> int:
        return len(self.basis)

    def generator(self, i: int) -> np.ndarray:
        """sigma_i, positive exchange of positions i and i+1 (1-indexed)."""
        if not 1 <= i < self.number:
            raise ValueError("braid index must be between 1 and number-1")
        if i not in self._generators:
            path = _rotation_path(self.tree, i - 1)
            target = path[-1]
            U = path_map(self.model, path, self.labels, self.total)
            destination_basis = fusion_basis(self.model, target, self.labels, self.total)
            fused = frozenset((i - 1, i))
            D = np.diag([self.model.R(self.charge, self.charge, s[fused])
                         for s in destination_basis])
            self._generators[i] = U.conj().T @ D @ U
        return self._generators[i].copy()

    def word(self, letters: list[int] | tuple[int, ...]) -> np.ndarray:
        """Left-to-right application of generators. Negative i means inverse."""
        matrix = np.eye(self.dimension, dtype=complex)
        for letter in letters:
            if letter == 0:
                raise ValueError("generator zero is invalid")
            G = self.generator(abs(letter))
            matrix = (G if letter > 0 else G.conj().T) @ matrix
        return matrix

    def relations(self) -> dict[str, float]:
        """Max residuals for unitarity, Yang-Baxter and distant commutation."""
        G = [self.generator(i) for i in range(1, self.number)]
        ident = np.eye(self.dimension)
        errors = {"unitarity": 0.0, "yang_baxter": 0.0, "far_commutation": 0.0}
        def err(A, B):
            return float(np.max(np.abs(A-B)))
        for a in G:
            errors["unitarity"] = max(errors["unitarity"], err(a.conj().T @ a, ident))
        for i in range(len(G)-1):
            a,b = G[i:i+2]
            errors["yang_baxter"] = max(errors["yang_baxter"], err(a@b@a, b@a@b))
        for i in range(len(G)):
            for j in range(i+2, len(G)):
                a,b = G[i],G[j]
                errors["far_commutation"] = max(errors["far_commutation"], err(a@b,b@a))
        return errors


def matrix_json(A: np.ndarray, decimals: int = 12) -> list[list[list[float]]]:
    """Portable JSON encoding: each complex entry is [real,imag]."""
    return [[[round(float(z.real), decimals), round(float(z.imag), decimals)]
             for z in row] for row in A]
