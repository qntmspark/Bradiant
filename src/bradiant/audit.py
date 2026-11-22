"""Independent graphical-coherence audits on every sector of a finite model."""
from dataclasses import dataclass, asdict
from itertools import product
import numpy as np
from .model import FusionModel
from .trees import path_map


@dataclass(frozen=True)
class AuditResult:
    model: str
    f_unitarity_residual: float
    r_unitarity_residual: float
    unit_residual: float
    pentagon_residual: float
    hexagon_residual: float
    f_sectors: int
    pentagon_sectors: int
    hexagon_sectors: int
    tolerance: float
    worst_pentagon_sector: tuple[str, str, str, str, str] | None = None
    worst_hexagon_sector: tuple[str, str, str, str, str] | None = None

    @property
    def passed(self) -> bool:
        return max(self.f_unitarity_residual, self.r_unitarity_residual,
                   self.unit_residual, self.pentagon_residual,
                   self.hexagon_residual) <= self.tolerance

    def to_dict(self) -> dict:
        return {**asdict(self), "passed": self.passed}


def _residual(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape:
        return float("inf")
    return float(np.max(np.abs(a - b))) if a.size else 0.0


def audit(model: FusionModel, *, tol: float = 1e-10) -> AuditResult:
    """Check all F unitarity, all R magnitudes, pentagon and both hexagons.

    Enumerates all external charge quadruples/triples and all total sectors.
    Computational cost grows as O(r^5 * fusion-path-dimension^3) in rank r.
    No unpublished tolerance adjustments or sampling are performed.
    """
    if not np.isfinite(tol) or tol <= 0:
        raise ValueError("tol must be finite and positive")
    f_err = r_err = unit_err = pent_err = hex_err = 0.0
    worst_pentagon = worst_hexagon = None
    fs = ps = hs = 0
    C = model.charges
    for a, b, c, d in product(C, repeat=4):
        f = model.f_matrix(a, b, c, d)
        if f.size:
            fs += 1
            f_err = max(f_err, _residual(f @ f.conj().T, np.eye(f.shape[0])))
            if model.unit in (a, b, c):
                unit_err = max(unit_err, _residual(f, np.eye(f.shape[0])))
    for (a, b, _), val in model.r_symbols.items():
        r_err = max(r_err, abs(abs(val) - 1))
        if model.unit in (a, b):
            unit_err = max(unit_err, abs(val - 1))
    for a, b, c, d, total in product(C, repeat=5):
        labels = (a, b, c, d)
        t0 = (((0, 1), 2), 3)
        t1 = ((0, (1, 2)), 3)
        t2 = (0, ((1, 2), 3))
        t3 = (0, (1, (2, 3)))
        t4 = ((0, 1), (2, 3))
        lhs = path_map(model, [t0, t1, t2, t3], labels, total)
        rhs = path_map(model, [t0, t4, t3], labels, total)
        if lhs.size:
            ps += 1
            sector_err = _residual(lhs, rhs)
            if sector_err > pent_err:
                pent_err = sector_err
                worst_pentagon = (a, b, c, d, total)
    for a, b, c, total in product(C, repeat=4):
        labels = (a, b, c)
        start = (0, (1, 2))
        end = ((1, 2), 0)
        direct = path_map(model, [start, end], labels, total)
        indirect = path_map(model, [start, ((0, 1), 2), ((1, 0), 2),
                                    (1, (0, 2)), (1, (2, 0)), end], labels, total)
        if direct.size:
            hs += 1
            sector_err = _residual(direct, indirect)
            if sector_err > hex_err:
                hex_err = sector_err
                worst_hexagon = ("first", a, b, c, total)
        start = ((0, 1), 2)
        end = (2, (0, 1))
        direct = path_map(model, [start, end], labels, total)
        indirect = path_map(model, [start, (0, (1, 2)), (0, (2, 1)),
                                    ((0, 2), 1), ((2, 0), 1), end], labels, total)
        if direct.size:
            hs += 1
            sector_err = _residual(direct, indirect)
            if sector_err > hex_err:
                hex_err = sector_err
                worst_hexagon = ("second", a, b, c, total)
    return AuditResult(model.name, f_err, r_err, unit_err, pent_err, hex_err,
                       fs, ps, hs, tol, worst_pentagon, worst_hexagon)
