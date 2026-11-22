import cmath
import math
import pytest
from braidiant import (audit, fibonacci, ising, cyclic, regauge,
                       FusionModel, ModelError)


@pytest.mark.parametrize("factory", [fibonacci, ising, cyclic])
def test_known_coherent_models(factory):
    result = audit(factory())
    assert result.passed, result
    assert result.pentagon_sectors > 0
    assert result.hexagon_sectors > 0
    assert result.pentagon_residual < 1e-12
    assert result.hexagon_residual < 1e-12


def test_fibonacci_reference_symbols():
    m = fibonacci()
    phi = (1 + math.sqrt(5)) / 2
    f = m.f_matrix("tau", "tau", "tau", "tau")
    assert f.shape == (2, 2)
    assert abs(f[0, 0] - 1 / phi) < 1e-14
    assert abs(f[1, 1] + 1 / phi) < 1e-14
    assert abs(m.R("tau", "tau", "1") - cmath.exp(-4j * math.pi / 5)) < 1e-14


def test_ising_reference_symbols():
    m = ising()
    f = m.f_matrix("sigma", "sigma", "sigma", "sigma")
    assert abs(f[0, 0] - 1 / math.sqrt(2)) < 1e-14
    assert abs(f[1, 1] + 1 / math.sqrt(2)) < 1e-14
    assert m.fuse("sigma", "sigma") == ("1", "psi")


def test_rephasing_preserves_coherence_nonabelian():
    m = fibonacci()
    gm = regauge(m, {("tau", "tau", "tau"): cmath.exp(1.17j),
                     ("tau", "tau", "1"): cmath.exp(0.39j)})
    assert audit(gm).passed
    assert gm.f_matrix("tau", "tau", "tau", "tau")[0, 1] != \
           m.f_matrix("tau", "tau", "tau", "tau")[0, 1]


def test_rephasing_preserves_coherence_abelian():
    gm = regauge(cyclic(3), {("1", "2", "0"): cmath.exp(0.4j)})
    assert audit(gm).passed
    assert gm.R("1", "2", "0") != gm.R("2", "1", "0")


def test_mutated_unitary_r_detected_by_hexagon():
    m = fibonacci()
    R = dict(m.r_symbols)
    R["tau", "tau", "1"] *= cmath.exp(0.12j)
    corrupted = FusionModel("corrupted R", m.charges, m.unit, m.fusion, m.f_symbols, R)
    check = audit(corrupted)
    assert check.r_unitarity_residual < 1e-12
    assert check.hexagon_residual > 0.01
    assert not check.passed


def test_mutated_f_detected_by_unitarity_and_pentagon():
    m = fibonacci()
    F = dict(m.f_symbols)
    key = ("tau", "tau", "tau", "tau", "1", "1")
    F[key] *= 1.01
    altered = FusionModel("corrupt F", m.charges, m.unit, m.fusion, F, m.r_symbols)
    check = audit(altered)
    assert check.f_unitarity_residual > 1e-3
    assert check.pentagon_residual > 1e-3
    assert not check.passed


def test_bad_fusion_rejected():
    m = fibonacci()
    fusion = dict(m.fusion)
    fusion["tau", "1"] = ("1",)
    with pytest.raises(ModelError):
        FusionModel("bad", m.charges, m.unit, fusion, m.f_symbols, m.r_symbols)


def test_missing_f_symbol_rejected():
    m = fibonacci()
    F = dict(m.f_symbols)
    F.pop(next(iter(F)))
    with pytest.raises(ModelError, match="F symbol missing"):
        FusionModel("bad", m.charges, m.unit, m.fusion, F, m.r_symbols)


def test_bad_tolerance_rejected():
    with pytest.raises(ValueError):
        audit(fibonacci(), tol=-1)


@pytest.mark.parametrize("n", [2, 3, 4, 5])
def test_pointed_models(n):
    assert audit(cyclic(n, 1)).passed
