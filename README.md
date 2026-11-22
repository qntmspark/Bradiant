<div align="center">
  <img src="assets/bradiant-logo.png" width="360" alt="Bradiant, original black B braid mark and lowercase wordmark">

  # Bradiant

  **Auditable anyon data. Reproducible braids.**

  A lightweight, open-source Python research library for checking numerical fusion-category
  consistency and constructing finite-dimensional anyonic braid representations.
</div>

---

## Why Bradiant?

An anyon model is not determined merely by its fusion rules. Its associators (F symbols)
and exchanges (R symbols) must satisfy stringent algebraic identities before numerical
braiding predictions can be trusted. Conventions, phases, category gauge changes and
fusion-tree indexing can create subtle errors, even in small models.

**Bradiant** provides an independent, inspectable path from raw F/R tables to
**exhaustively enumerated numerical coherence tests** for a finite multiplicity-free
model, and then to braid matrices, braid words and reproducible JSON records.

This is a **software verification tool**, not a hardware experiment or a claim of
machine-checked mathematical proof. Floating-point residuals diagnose the supplied
numerical data to the stated tolerance.

## Capabilities

- Validate fusion-table completeness, the tensor unit, rigid duals, commutativity and fusion associativity.
- Check F-block unitarity, R-symbol unimodularity and strict tensor-unit normalization.
- Compute Frobenius–Perron dimensions, global dimension, categorical duals,
  gauge-invariant monodromy and transparent objects (when input coherence is satisfied).
- Enumerate **all** charge sectors of both pentagon and both hexagon identities.
- Construct the braid group generators on homogeneous fusion-path Hilbert spaces.
- Check Yang–Baxter, distant-generator commutation and unitary inverse relations.
- Rephase fusion vertices and confirm gauge-covariant consistency.
- Import and export explicitly specified, versioned JSON F/R data and
  SHA-256-fingerprinted computational reports.
- Produce machine-readable diagnostics for independent reproduction and regression testing.
- Start from documented reference models: Fibonacci, Ising, and pointed cyclic Z_n models.

## Quick start

Requires Python 3.10 or later. Clone the repository or unpack a source release, then run:

```bash
python -m pip install -e '.[dev]'
python -m pytest
bradiant audit
bradiant --model ising audit
bradiant --model cyclic --n 3 audit
bradiant --model ising invariants
bradiant braid --charge tau --anyons 4 --total 1 --word 1,-2,1
```

The command prints JSON and returns a nonzero status if an audit fails the specified
tolerance. The positive braid generator `i` exchanges positions `i` and `i+1`;
a negative integer denotes its inverse. Command-line flags `--model`, `--model-file`,
`--tol` and `--output` precede the subcommand.

### Python API

```python
from bradiant import fibonacci, audit, BraidRepresentation

model = fibonacci()
result = audit(model, tol=1e-10)
assert result.passed

braids = BraidRepresentation(model, charge="tau", number=4, total="1")
assert braids.dimension == 2
print(braids.generator(2))
print(braids.word([1, -2, 1]))
print(braids.relations())

from bradiant import fusion_invariants, braiding_invariants
print(fusion_invariants(model).to_dict())
print(braiding_invariants(model).transparent_charges)
```

### Load your own fusion model

```python
from bradiant import load_model, audit, save_model, fibonacci
save_model(fibonacci(), "fibonacci.json")
model = load_model("fibonacci.json")
print(audit(model).to_dict())
```

The JSON schema uses `charges`, `unit`, `fusion`, `F`, `R`, `schema_version: 1`,
and each complex entry is represented by its real and imaginary parts. See
[`docs/model_format.md`](docs/model_format.md) and
[`examples/fibonacci.json`](examples/fibonacci.json) for the exact ordering.

The former `braidiant` import and command remain supported as compatibility aliases.

## Reproduce the verification data

```bash
python examples/reproduce.py > reproduced.json
python examples/benchmark.py --repeats 7 > local_benchmark.json
python -m pytest
```

The repository includes a reference JSON report at
[`examples/reference_results.json`](examples/reference_results.json), generated
from actual numerical code execution. Tiny residual differences between NumPy/platform
versions are expected; use the numerical tolerance, not byte-for-byte equality.

| Built-in model | Pentagon sectors checked | Hexagon sectors checked | Typical max numerical residual |
|---|---:|---:|---:|
| Fibonacci | 27 | 24 | below 1e-12 |
| Ising | 106 | 66 | below 1e-12 |
| Cyclic Z₃ | 81 | 54 | below 1e-12 |

All figures are from the bundled computations, **not from quantum hardware**.

## Scientific conventions and limits

The core currently supports finite, **unitary, multiplicity-free, braided** fusion
data. F-matrices are defined for `((a b)_e c)_d -> (a (b c)_f)_d`, with entries
`F[a,b,c,d,e,f]`. Their physical gauge is explicit. The implementation does
**not** calculate tensor categories from generators, find F/R solutions, certify
symbolic equalities, treat fusion multiplicities above one, or implement
noise models, decoders, experimental control or arbitrarily many anyons.
Braid representations use identical external charges and up to nine anyons;
exact limits depend on the exponential dimension of fusion spaces.

See [`docs/mathematics.md`](docs/mathematics.md) and
[`docs/reproducibility.md`](docs/reproducibility.md).

## Computational and scientific rigor

The release includes numerical reference checks of the golden-ratio Fibonacci
quantum dimension, Ising quantum dimension √2, known double-braiding phases,
expected transparent objects in cyclic models, random gauge rephasings, direct
three-anyon braid formulas and deliberately corrupted F/R inputs. The model
loader rejects unused symbols and non-rigid fusion rules; the CLI refuses to
construct braid matrices when an input fails coherence tests. The reference
report is generated by an executable script; the benchmark script reports
machine-local wall-clock times without claiming speed superiority.

The package offers *numerical evidence*, not a formal proof or a replacement
for independent expert review. See [`docs/mathematics.md`](docs/mathematics.md),
[`docs/architecture.md`](docs/architecture.md),
[`docs/comparison.md`](docs/comparison.md) and
[`docs/reproducibility.md`](docs/reproducibility.md).

## Relationship to existing tools

[Anyonica](https://github.com/gert-vercleyen/Anyonica) is aimed at finding and
classifying fusion-category data; [TQSim](https://github.com/Constantine-Quantum-Tech/tqsim)
provides anyonic quantum-circuit simulation.
[TensorCategories.jl](https://tensorcategories.github.io/TensorCategories.jl/stable/)
implements broader symbolic and numerical tensor-category operations.
Bradiant is scoped as an
independent, table-driven *audit* and braid-representation library, with all
sector-level identities checked, JSON input/output, and deliberate corruption
regression tests. This is a complementary focus, not a claim of superior speed or
coverage, and no systematic performance comparison has yet been made.

## Open development and publication status

Version **0.2.1** is a research-software development release. The included
[`paper.md`](paper.md) is a **JOSS preparation draft**, not a submitted or
accepted JOSS article. The current JOSS editorial gate requires more than six
months of public, active, iterative development, demonstrated research use,
and documented open-source practices. See [`docs/joss_readiness.md`](docs/joss_readiness.md).

The package is MIT licensed. Contributions and independently reproduced results
are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md). Project support is via GitHub
issues. Please cite the software via the repository URL until a permanent archive
DOI exists. The package is not claimed to be deployed on PyPI or accepted by a journal.