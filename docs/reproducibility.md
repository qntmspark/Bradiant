# Reproducibility protocol

## Environment

- Python >= 3.10; NumPy >= 1.24. Continuous integration tests Python 3.10-3.13.
- Python packages specified in `pyproject.toml`, no compiled category solver,
  network connection, proprietary quantum cloud credentials or hardware required.
- All reference data stored in `examples/`. No random seeds or hidden datasets.

## Procedure

```bash
python -m pip install -e '.[dev]'
python -m pytest
python examples/reproduce.py > new_results.json
braidiant --model-file examples/fibonacci.json audit
braidiant --model-file examples/ising.json audit
braidiant --model cyclic --n 3 audit
braidiant braid --charge tau --anyons 4 --total 1 --word 1,-2,1
```

`examples/reference_results.json` is a *sample execution artifact* with measured
numerical residuals and sector counts; it was produced by running the included
code, not inserted as an assumed expected outcome. Floating-point residuals
may vary slightly by environment, so compare against the specified tolerance.

## Trust and validation

- Baselines: hard-coded published Fibonacci and Ising symbols and independent
  expected fusion dimensions / eigenphases in the tests.
- Model mutation tests: one perturbed R phase, which leaves its magnitude
  equal to one but causes a hexagon failure; one altered F symbol, which
  causes both a pentagon and unitary failure.
- Nontrivial gauge changes: valid category data remain coherent, while
  braid-matrix eigenvalues remain unchanged.
- Versioned JSON read-write round trips, CLI invocation and smoke testing.

This is mathematical *simulation and consistency checking*. No real quantum
processor or photonic apparatus was used. Runtime benchmarks and comparison
to competing tools are not yet claimed.

## Extending benchmark evidence

Before submission to a research software journal, add more independently
sourced category data, cross-validate the implementations against a separate
library where possible, and collect external reproduction reports. Expand
CI to cover larger representative models and store revision-tagged results.
