"""Independent analytic or gauge-covariant reference checks for invariants."""
import cmath
import math
import random
import subprocess
import sys
import json
import numpy as np
import pytest

from bradiant import (FusionModel, ModelError, fibonacci, ising, cyclic, regauge,
                       fusion_invariants, fusion_matrices, braiding_invariants, audit,
                       BraidRepresentation)


def _lookup(result, a, b, channel):
    values = [complex(row["real"], row["imag"]) for row in result.monodromies
              if (row["a"], row["b"], row["channel"]) == (a, b, channel)]
    assert len(values) == 1
    return values[0]


def test_fibonacci_fp_dimensions_and_monodromy():
    model = fibonacci()
    ring = fusion_invariants(model)
    phi = (1 + math.sqrt(5)) / 2
    assert ring.dimensions["1"] == pytest.approx(1)
    assert ring.dimensions["tau"] == pytest.approx(phi)
    assert ring.global_dimension == pytest.approx(1 + phi ** 2)
    assert ring.duals == {"1": "1", "tau": "tau"}
    m = braiding_invariants(model)
    assert m.transparent_charges == ["1"]
    assert _lookup(m, "tau", "tau", "1") == pytest.approx(cmath.exp(-8j * math.pi / 5))
    assert _lookup(m, "tau", "tau", "tau") == pytest.approx(cmath.exp(6j * math.pi / 5))


def test_ising_fp_dimensions_and_monodromy():
    ring = fusion_invariants(ising())
    assert ring.dimensions["sigma"] == pytest.approx(math.sqrt(2))
    assert ring.dimensions["psi"] == pytest.approx(1)
    assert ring.global_dimension == pytest.approx(4)
    m = braiding_invariants(ising())
    assert m.transparent_charges == ["1"]
    assert _lookup(m, "sigma", "sigma", "1") == pytest.approx(cmath.exp(-1j * math.pi / 4))
    assert _lookup(m, "sigma", "sigma", "psi") == pytest.approx(cmath.exp(3j * math.pi / 4))


@pytest.mark.parametrize("n,k,center", [(2,1,["0","1"]), (3,1,["0"]),
                                        (4,1,["0","2"]), (5,1,["0"]),
                                        (6,1,["0","3"]), (6,0,[str(i) for i in range(6)])])
def test_cyclic_transparent_charges(n,k,center):
    model = cyclic(n,k)
    inv = fusion_invariants(model)
    assert inv.global_dimension == pytest.approx(n)
    assert all(v == pytest.approx(1) for v in inv.dimensions.values())
    assert braiding_invariants(model).transparent_charges == center


@pytest.mark.parametrize("model", [fibonacci(), ising(), cyclic(3), cyclic(4)])
def test_fusion_matrices_act_on_fp_dimension_vector(model):
    dims = fusion_invariants(model).dimensions
    v = np.array([dims[x] for x in model.charges])
    for a, matrix in fusion_matrices(model).items():
        assert np.allclose(matrix @ v, dims[a] * v, atol=1e-12)


@pytest.mark.parametrize("model", [fibonacci(), ising(), cyclic(3)])
def test_monodromy_invariant_under_random_rephasing(model):
    rng = random.Random(2031)
    phases = {(a,b,c): cmath.exp(1j*rng.uniform(-math.pi,math.pi))
              for a in model.charges for b in model.charges for c in model.fuse(a,b)
              if a != model.unit and b != model.unit}
    shifted = regauge(model, phases)
    assert audit(shifted).passed
    before = braiding_invariants(model)
    after = braiding_invariants(shifted)
    assert before.transparent_charges == after.transparent_charges
    assert len(before.monodromies) == len(after.monodromies)
    for x,y in zip(before.monodromies,after.monodromies):
        assert x["real"] == pytest.approx(y["real"],abs=1e-12)
        assert x["imag"] == pytest.approx(y["imag"],abs=1e-12)
    assert fusion_invariants(model).dimensions == pytest.approx(
        fusion_invariants(shifted).dimensions)


def test_reject_nonrigid_ring():
    bad = {("1","1"):("1",), ("1","x"):("x",),
           ("x","1"):("x",), ("x","x"):("x",)}
    with pytest.raises(ModelError, match="unique dual"):
        FusionModel("nonrigid", ("1","x"), "1", bad, {},
                    {(a,b,c):1 for (a,b), outputs in bad.items() for c in outputs})


def test_reject_unused_gauge_dependent_symbols():
    model = fibonacci()
    R = dict(model.r_symbols)
    R["1","tau","1"] = 1
    with pytest.raises(ModelError, match="unexpected"):
        FusionModel("extra R", model.charges, model.unit, model.fusion, model.f_symbols, R)
    F = dict(model.f_symbols)
    F["1","1","1","tau","1","1"] = 1
    with pytest.raises(ModelError, match="unexpected"):
        FusionModel("extra F", model.charges, model.unit, model.fusion, F, model.r_symbols)


def test_unit_normalization_is_audited():
    model = fibonacci()
    F = dict(model.f_symbols)
    key = ("1", "tau", "tau", "1", "tau", "1")
    assert key in F
    F[key] *= cmath.exp(0.23j)
    incorrect = FusionModel("unit error",model.charges,model.unit,model.fusion,F,model.r_symbols)
    check = audit(incorrect)
    assert check.f_unitarity_residual < 1e-12
    assert check.unit_residual > 0.1
    assert not check.passed


def test_cli_invariant_report(tmp_path):
    command = [sys.executable,"-m","bradiant", "--model","ising", "invariants"]
    outcome = subprocess.run(command, check=True, capture_output=True, text=True)
    data = json.loads(outcome.stdout)
    assert data["type"] == "invariants"
    assert data["audit"]["passed"]
    assert data["fusion"]["global_dimension"] == pytest.approx(4)
    assert data["braiding"]["transparent_charges"] == ["1"]
    assert len(data["model_sha256"]) == 64


def test_cli_refuses_inconsistent_braids(tmp_path):
    from bradiant import save_model
    m = fibonacci()
    R = dict(m.r_symbols)
    R["tau","tau","1"] *= cmath.exp(0.12j)
    path = tmp_path / "bad.json"
    save_model(FusionModel("bad",m.charges,m.unit,m.fusion,m.f_symbols,R),path)
    command = [sys.executable,"-m","bradiant","--model-file",str(path),"braid"]
    result = subprocess.run(command, capture_output=True,text=True)
    assert result.returncode != 0
    assert "fails the numerical coherence audit" in result.stderr


def test_independent_fibonacci_three_anyon_formula():
    model = fibonacci()
    rep = BraidRepresentation(model,"tau",3,"tau")
    F = model.f_matrix("tau","tau","tau","tau")
    R = np.diag([model.R("tau","tau",c) for c in ("1","tau")])
    assert np.allclose(rep.generator(1),R,atol=1e-13)
    assert np.allclose(rep.generator(2),F.conj().T @ R @ F,atol=1e-13)


def test_braid_word_inverse_and_determinant():
    rep = BraidRepresentation(fibonacci(),"tau",5,"tau")
    word = [1,-2,3,4,-1,2,3,-4]
    inverse = [-i for i in reversed(word)]
    assert np.allclose(rep.word(inverse) @ rep.word(word),np.eye(rep.dimension),atol=1e-12)
    assert abs(abs(np.linalg.det(rep.word(word))) - 1) < 1e-12
