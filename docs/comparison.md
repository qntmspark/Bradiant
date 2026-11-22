# Comparison with related software

This comparison was grounded in the projects' publicly documented scope,
not a claim of feature superiority. Versions and APIs may change.

| Software | Primary objective | Languages and style | Bradiant distinction |
|---|---|---|---|
| [Anyonica](https://github.com/gert-vercleyen/Anyonica) | Classify and manipulate fusion rings and category data; solve coherence constraints | Wolfram Language / Mathematica | Accept complete numeric F/R tables and produce independent residual audits, not symbolic solutions |
| [TensorCategories.jl](https://tensorcategories.github.io/TensorCategories.jl/stable/) | General tensor/fusion category computations, exact algebra, databases, numerical models | Julia/OSCAR | Small Python, minimal dependency, explicit JSON verification workflow rather than a competing general category framework |
| [TQSim](https://github.com/Constantine-Quantum-Tech/tqsim) | Simulate Fibonacci anyon circuits | Python | Verify category data and construct model-agnostic braid matrices, not sample anyonic circuits |
| [tqec](https://joss.theoj.org/papers/10.21105/joss.09142) | Topological quantum error-correction software | Python | Topological QEC compilation has a different remit from fusion-category coherence diagnostics |

## Why a distinct package?

There is substantial overlap with the existing tensor-category ecosystem,
particularly with TensorCategories.jl, which itself exposes coherence
verification. Bradiant's narrower scientific interface is a deliberately
lightweight Python audit of portable F/R tables, with independent unit tests,
explicit gauge conventions, deterministic signatures and a small matrix
representation API. That workflow is useful in Python-only experiments and
cross-checks against a separate symbolic system.

This is **not** evidence that existing tools cannot solve the same problems,
and no quantitative speed comparison or interoperability with those tools
has yet been demonstrated. A formal JOSS submission should report an actual
external reproduction/interop case or other independently verifiable use;
the existence of a Python wrapper alone is not a sufficient research claim.

Sources consulted in November 2026: package repositories, the
2026 Vercleyen--Slingerland *Communications in Mathematical Physics* study,
TensorCategories.jl stable docs, and the published JOSS `tqec` software article.
