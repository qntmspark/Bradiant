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
python examples/benchmark.py --repeats 7 > local_timings.json
bradiant --model ising invariants
bradiant --model-file examples/fibonacci.json audit
bradiant --model-file examples/ising.json audit
bradiant --model cyclic --n 3 audit
bradiant braid --charge tau --anyons 4 --total 1 --word 1,-2,1
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
- Independent analytic FP dimension and channel monodromy checks for Fibonacci,
  chiral Ising and pointed cyclic data, including degenerate cyclic examples.
- Random nontrivial vertex-gauge rephasings, a strict unit-normalization failure,
  and missing/extra data rejection.
- SHA-256 model fingerprints attach reports to an explicit gauge and entry order.

This is mathematical *simulation and consistency checking*. No real quantum
processor or photonic apparatus was used. The benchmark script records local runtime measurements
but does not claim speed or functionality superiority to competing tools.

## Extending benchmark evidence

Before submission to a research software journal, add more independently
sourced category data, cross-validate the implementations against a separate
library where possible, and collect external reproduction reports. Expand
CI to cover larger representative models and store revision-tagged results.
