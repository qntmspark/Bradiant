"""Fusion-tree enumerator and elementary associator/braiding maps.

Tree leaves are distinct integer *identities*, not charge labels.
Tree nodes are pairs; keys are frozensets of leaf identities. A rotation
or swap changes topology/order, while retaining all unaffected sector labels.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Iterator
import numpy as np
from .model import FusionModel, ModelError

Tree = int | tuple["Tree", "Tree"]


def leaf_ids(t: Tree) -> frozenset[int]:
    if isinstance(t, int):
        return frozenset((t,))
    return leaf_ids(t[0]) | leaf_ids(t[1])


def canonical_key(state: dict[frozenset[int], str]) -> tuple:
    return tuple(sorted((tuple(sorted(k)), v) for k, v in state.items()))


def fusion_basis(model: FusionModel, tree: Tree, labels: tuple[str, ...],
                 total: str) -> list[dict[frozenset[int], str]]:
    """Enumerate fusion-path basis states in a deterministic order."""
    if len(leaf_ids(tree)) != len(labels) or leaf_ids(tree) != frozenset(range(len(labels))):
        raise ModelError("tree leaves must be 0,...,N-1, each exactly once")

    def walk(t: Tree) -> list[tuple[str, dict[frozenset[int], str]]]:
        if isinstance(t, int):
            return [(labels[t], {frozenset((t,)): labels[t]})]
        pairs = []
        for (a, m1), (b, m2) in product(walk(t[0]), walk(t[1])):
            for c in model.fuse(a, b):
                pairs.append((c, {**m1, **m2, leaf_ids(t): c}))
        return pairs

    return sorted((m for c, m in walk(tree) if c == total), key=canonical_key)


def _match_rotate(before: Tree, after: Tree):
    """Return (A,B,C,removed_key,added_key), for exactly one rightward rotation."""
    if not isinstance(before, tuple) or not isinstance(after, tuple):
        return None
    if (isinstance(before[0], tuple) and isinstance(after[1], tuple)
            and before[0][0] == after[0]
            and before[0][1] == after[1][0]
            and before[1] == after[1][1]):
        a, b, c = before[0][0], before[0][1], before[1]
        return a, b, c, leaf_ids(before[0]), leaf_ids(after[1])
    if before[1] == after[1]:
        return _match_rotate(before[0], after[0])
    if before[0] == after[0]:
        return _match_rotate(before[1], after[1])
    return None


def _match_swap(before: Tree, after: Tree):
    if not isinstance(before, tuple) or not isinstance(after, tuple):
        return None
    if before[0] == after[1] and before[1] == after[0]:
        return before[0], before[1], leaf_ids(before)
    if before[1] == after[1]:
        return _match_swap(before[0], after[0])
    if before[0] == after[0]:
        return _match_swap(before[1], after[1])
    return None


def elementary_map(model: FusionModel, before: Tree, after: Tree,
                   labels: tuple[str, ...], total: str) -> np.ndarray:
    """Map source basis column vectors into target basis vectors.

    Supports exactly one right/left associator rotation or one local swap.
    Rotation convention: (target_f,source_e) = F[e,f].
    """
    src = fusion_basis(model, before, labels, total)
    dst = fusion_basis(model, after, labels, total)
    out = np.zeros((len(dst), len(src)), dtype=complex)
    direct = _match_rotate(before, after)
    reverse = False
    if direct is None:
        direct = _match_rotate(after, before)
        reverse = direct is not None
    if direct is not None:
        a, b, c, oldkey, newkey = direct
        for i, d in enumerate(dst):
            for j, s in enumerate(src):
                # In both directions, exactly one intermediate label changes.
                exclude = {oldkey, newkey}
                if any(s.get(k) != d.get(k) for k in set(s) & set(d) if k not in exclude):
                    continue
                sector = s if not reverse else d
                other = d if not reverse else s
                alpha, beta, gamma = (sector[leaf_ids(x)] for x in (a, b, c))
                out_charge = sector[leaf_ids((a, (b, c)))]
                e = sector[oldkey]
                f = other[newkey]
                value = model.F(alpha, beta, gamma, out_charge, e, f)
                out[i, j] = value if not reverse else value.conjugate()
        return out
    swapped = _match_swap(before, after)
    if swapped is None:
        raise ModelError("trees must differ by precisely one rotation or local swap")
    a, b, root = swapped
    for i, d in enumerate(dst):
        for j, s in enumerate(src):
            if canonical_key(s) != canonical_key(d):
                continue
            out[i, j] = model.R(s[leaf_ids(a)], s[leaf_ids(b)], s[root])
    return out


def path_map(model: FusionModel, trees: list[Tree], labels: tuple[str, ...],
             total: str) -> np.ndarray:
    """Compose elementary recouplings/braidings left to right in a path."""
    width = len(fusion_basis(model, trees[0], labels, total))
    result = np.eye(width, dtype=complex)
    for old, new in zip(trees, trees[1:]):
        result = elementary_map(model, old, new, labels, total) @ result
    return result


def all_binary_trees(leaves: tuple[int, ...]) -> tuple[Tree, ...]:
    """All planar binary trees on the supplied ordered leaves (Catalan many)."""
    if len(leaves) == 1:
        return (leaves[0],)
    result = []
    for split in range(1, len(leaves)):
        for a in all_binary_trees(leaves[:split]):
            for b in all_binary_trees(leaves[split:]):
                result.append((a, b))
    return tuple(result)


def right_rotations(tree: Tree) -> Iterator[Tree]:
    """All single reassociations of a tree, in both directions."""
    if not isinstance(tree, tuple):
        return
    left, right = tree
    if isinstance(left, tuple):
        yield (left[0], (left[1], right))
    if isinstance(right, tuple):
        yield ((left, right[0]), right[1])
    for x in right_rotations(left):
        yield (x, right)
    for x in right_rotations(right):
        yield (left, x)
