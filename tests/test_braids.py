import numpy as np
import pytest
from braidiant import fibonacci, ising, cyclic, regauge, BraidRepresentation


@pytest.mark.parametrize("model,charge,total,n,expected", [
    (fibonacci(), "tau", "tau", 3, 2),
    (fibonacci(), "tau", "1", 4, 2),
    (fibonacci(), "tau", "tau", 5, 5),
    (fibonacci(), "tau", "1", 6, 5),
    (ising(), "sigma", "sigma", 3, 2),
    (ising(), "sigma", "1", 4, 2),
    (ising(), "sigma", "sigma", 5, 4),
    (ising(), "sigma", "1", 6, 4),
    (cyclic(3), "1", "0", 3, 1),
])
def test_generators_obey_braid_relations(model, charge, total, n, expected):
    r = BraidRepresentation(model, charge, n, total)
    assert r.dimension == expected
    assert max(r.relations().values()) < 1e-12
    assert np.allclose(r.word([1, -1]), np.eye(expected), atol=1e-12)
    assert np.allclose(r.word([1, 2, 1]), r.word([2, 1, 2]), atol=1e-12)


def test_nonabelian_braid_generators_do_not_commute():
    r = BraidRepresentation(fibonacci(), "tau", 3, "tau")
    a, b = r.generator(1), r.generator(2)
    assert np.max(np.abs(a @ b - b @ a)) > 0.1


def test_ising_sigma_spectrum():
    r = BraidRepresentation(ising(), "sigma", 4, "1")
    eigenvalues = np.linalg.eigvals(r.generator(1))
    expected = [ising().R("sigma", "sigma", t) for t in ("1", "psi")]
    assert np.allclose(sorted(eigenvalues, key=lambda z: z.real),
                       sorted(expected, key=lambda z: z.real))


def test_gauge_preserves_braid_eigenvalues():
    original = fibonacci()
    gauge = regauge(original, {("tau", "tau", "1"): np.exp(0.45j),
                              ("tau", "tau", "tau"): np.exp(0.37j)})
    a = BraidRepresentation(original, "tau", 5, "tau")
    b = BraidRepresentation(gauge, "tau", 5, "tau")
    for i in range(1, 5):
        assert np.allclose(np.sort_complex(np.linalg.eigvals(a.generator(i))),
                           np.sort_complex(np.linalg.eigvals(b.generator(i))))


def test_bad_braid_words_rejected():
    r = BraidRepresentation(fibonacci(), "tau", 4, "1")
    with pytest.raises(ValueError):
        r.generator(4)
    with pytest.raises(ValueError):
        r.word([0])
    with pytest.raises(ValueError):
        BraidRepresentation(fibonacci(), "1", 2, "tau")
    with pytest.raises(ValueError):
        BraidRepresentation(fibonacci(), "tau", 10, "tau")
