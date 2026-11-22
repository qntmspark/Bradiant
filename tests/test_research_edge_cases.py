"""Additional provenance, input-error, and independent braid-representation checks."""
import cmath
import hashlib
import math
from pathlib import Path

import numpy as np
import pytest

from bradiant import BraidRepresentation, ModelError, audit, cyclic, fibonacci, ising
from bradiant.model import model_from_tables


def test_unknown_f_override_is_rejected():
    m = fibonacci()
    bogus = {("tau", "1", "tau", "1", "1", "tau"): 1}
    with pytest.raises(ModelError, match="nonexistent channel"):
        model_from_tables("bad", m.charges, m.unit, m.fusion, bogus, m.r_symbols)


@pytest.mark.parametrize("n,k", [(3,1), (4,1), (5,2)])
def test_cyclic_braid_generator_matches_analytic_bicharacter(n, k):
    model = cyclic(n, k)
    q = "1"
    total = str(3 % n)
    r = BraidRepresentation(model, q, 3, total)
    expected = cmath.exp(2j * math.pi * k / n)
    for i in (1, 2):
        assert np.allclose(r.generator(i), [[expected]], atol=1e-12)
    assert audit(model).passed


@pytest.mark.parametrize("name,model,charge,total", [
    ("Fibonacci", fibonacci(), "tau", "tau"),
    ("Ising", ising(), "sigma", "sigma"),
])
def test_braid_word_is_a_representation_of_group_composition(name, model, charge, total):
    r = BraidRepresentation(model, charge, 5, total)
    first = [1, -2, 3, -1]
    second = [-3, 4, 2, -1]
    assert np.allclose(r.word(first + second), r.word(second) @ r.word(first), atol=1e-12)


def test_logo_master_integrity():
    # Track original bytes to prevent accidental replacement with unrelated artwork.
    path = Path(__file__).resolve().parents[1] / "assets" / "bradiant-logo.png"
    assert path.exists()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == "1d14d1cfda143d649611c84d1542cbaad680963ed773cc0e9e8aa685a79fd870"
