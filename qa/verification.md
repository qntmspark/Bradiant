# Bradiant v0.3.0: verification and release note

**Scope:** Local numerical/scientific software validation and distribution checks. No hardware measurements or mathematical proof are claimed.

## Executed tests

- `PYTHONPATH=src python -m pytest -q`: 68 passed, 0 failures.
- Reference categories: Fibonacci, Ising and pointed cyclic $\mathbb{Z}_n$ models; pentagon/hexagon, unit, unitarity, braid-group consistency, Frobenius--Perron dimensions, monodromy, gauge changes, invalid inputs and JSON interchange.
- Independent expected quantities: $d_\tau=(1+\sqrt{5})/2$, $d_\sigma=\sqrt{2}$, $R_{\tau\tau}^{1}=e^{-4\pi i/5}$ and known pointed-model bicharacters.
- Deliberate input-corruption tests check failures rather than only successful examples.
- A separate pre-installation build and wheel installation test is performed during the release procedure.
- The original project-owner-supplied logo is preserved byte-for-byte (SHA-256 listed in `verification.json`).

## Interpretation

All checked numerical residuals are floating-point quantities. Tests do not prove the identities for arbitrary categories. The available reference models alone are not evidence of external research adoption, JOSS acceptance, or independent human scientific review.

## Reproduce

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python examples/reproduce.py > reproduced.json
python examples/benchmark.py --repeats 7 > machine_benchmark.json
bradiant audit
bradiant --model ising invariants
```

## Submission blockers

See `docs/joss_readiness.md` and `docs/submission_packet.md`. Current JOSS rules require active public development spanning more than six months, demonstrated research use, human validation and an accurate AI-use statement. No real JOSS DOI or submission is claimed.
