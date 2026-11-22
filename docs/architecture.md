# Architecture, interfaces and failure semantics

Bradiant treats **user-supplied numerical category data as untrusted input**.
The public library is split into four validation layers and two computational
consumers rather than a general-purpose simulation framework.

## Model validation (`model.py`)

`FusionModel` verifies a finite charge universe, two-sided vacuum, complete
multiplicity-free fusion table, commutative fusion, compatible associator
shapes, one simple dual per object, and complete/finite F- and R-symbol arrays.
Extra F/R records are rejected: a file with unused entries must not appear to
have been fully audited when those entries were silently ignored. This layer
checks **structural** conditions, not the numerical category coherence.

## Coherence (`audit.py` and `trees.py`)

The same tree-rotation/exchange matrix API represents both sides of every
pentagon and hexagon diagram. Comparing composed matrices rather than writing
index contractions explicitly reduces the chance of code diverging from the
graphical convention, at the cost of repeated finite-basis enumeration.
The audit checks every admissible four-charge pentagon and both three-charge
hexagon sectors; records the maximum entrywise residual and its charge sector;
and checks F unitarity, R magnitudes and strict tensor-unit normalization.

Failure is numerical: a diagnostic can pass while hiding defects smaller than
its tolerance. Conversely, a valid exact category may fail if evaluated with
inaccurate floating-point symbols. All reported numbers are double precision.

## Braid representations (`braid.py`)

For identical anyons with a fixed total charge, a breadth-first search finds
an associator path to a tree that locally fuses two adjacent positions.
The local exchange is diagonal in the intermediate fusion charge; conjugating
by the path map returns the generator to the left-associated reference basis.
The CLI audits the whole model before calculating a braid, avoiding plausible
but invalid results from known-inconsistent tables. The Python API exposes
building blocks and requires callers to audit their own input as appropriate.
The algorithm is bounded to 2–9 anyons because fusion spaces and binary-tree
search grow rapidly. Sparse/TN representations are beyond scope.

## Gauge-invariant diagnostics (`invariants.py`)

Fusion matrices give the Perron–Frobenius common eigenvector, normalized by
`d(unit)=1`, from which global squared dimension and the total dimension
are computed. In a unitary fusion category these FP dimensions equal the
quantum dimensions. Channel-wise monodromies `R_ab^c R_ba^c` are invariant
under rephasing of fusion vertices. Charge `a` is transparent if those phases
are one in every fusion channel for every `b`. This classifies the Müger
center **only for coherent braided input**. It does not determine an S matrix,
topological spins, pivotal structure or full modular data.

## Data interchange, CLI, scientific provenance

JSON files are strictly data-only (`io.py`) and include all allowed entries,
even allowed F entries with numerical value zero. The CLI serializes complex
numbers as `[real, imaginary]`, attaches a SHA-256 digest of the canonical
input table, and emits nonzero return statuses for failed audits. The digest
is deliberately gauge-sensitive: it identifies *input bytes normalized through
our schema*, not gauge-equivalence classes. Scripts in `examples/` regenerate
reference calculations and descriptive local timings.

## Deliberate limitations and future interfaces

The package does not solve for F/R data, model multiplicities above one,
certify exact algebraic equalities, simulate hardware, or quantify braiding
errors. It is intended to sit **between** category solvers/databases and
anyon-circuit simulators as a portable numerical cross-check. Cross-language
interop and independently sourced datasets are priority review items, not
features falsely advertised as already present.
