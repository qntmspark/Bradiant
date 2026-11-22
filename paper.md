---
title: 'Braidiant: Numerical coherence audits and braid representations for multiplicity-free anyon models'
tags:
  - Python
  - topological quantum computation
  - fusion categories
  - braid groups
  - numerical verification
authors:
  - name: 'AUTHOR NAME TO CONFIRM BEFORE SUBMISSION'
    affiliation: '1'
affiliations:
  - name: 'Affiliation to confirm (independent research if appropriate)'
    index: 1
date: 21 November 2026
bibliography: paper/references.bib
---

# Summary

Topological quantum computation encodes information in collective states of
quasiparticles, often called *anyons*, whose exchanges can implement quantum
operations. Specifying the possible outcomes of merging anyons does not by
itself provide a physically self-consistent computational model. The numerical
coefficients that control re-association and exchange must satisfy stringent
consistency equations. Small errors in a sign, a phase convention, or an
intermediate-charge ordering may lead to matrices that appear unitary but do
not describe coherent anyonic braiding.

**Braidiant** is an open-source Python library designed to make these checks
explicit and reproducible. Users can supply finite multiplicity-free fusion
rules and numerical associator (F) and exchange (R) coefficients, enumerate the
pentagon and two hexagon identities across every admissible charge sector,
and construct finite-dimensional braid-group representations in a fixed
fusion-path basis. Diagnostic residuals, matrix representations, and the
inputs are available in a machine-readable JSON format. The release includes
built-in Fibonacci, chiral Ising, and pointed cyclic models, along with a
command-line interface, a Python application programming interface, tests,
and an executable reference calculation.

# Statement of need

Anyon models play a foundational role in topological quantum computation,
quantum Hall research, and theoretical descriptions of non-Abelian
quasiparticles [@kitaev2006; @pachos2012]. Their associators and exchange
coefficients must satisfy coherence identities independently of any chosen
braiding sequence [@preskill2017]. This creates a practical verification
problem for researchers transferring tables from analytic calculations,
external datasets, or one software ecosystem to another. Even when the
underlying mathematics is standard, inconsistent gauge choices and implicit
index conventions can make independent reproduction difficult.

Braidiant targets researchers and advanced students who need a small,
inspectable numerical checker with deterministic output. Instead of requiring
a full anyonic circuit simulation environment, a model is described by a
versioned interchange format with explicit F and R records, including zero
entries inside allowed F blocks. The library checks unit objects, fusion
associativity, unitarity, and both families of coherence diagrams. Braid
matrices are constructed from generated fusion trees and local recoupling
moves, avoiding a catalog of hard-coded generator expressions for each number
of anyons. The resulting matrices can be exported for comparison against
independent derivations or downstream computational experiments.

# State of the field

There is a substantial existing ecosystem. **Anyonica** has been used to
construct, solve, and classify low-rank fusion-category data and has supported
a broad census of multiplicity-free fusion categories [@vercleyen2026].
**TQSim** focuses on topological quantum circuit simulation [@tqsim]. Other
packages for tensor categories and categorical datasets cover complementary
symbolic and structural methods [@anyonwiki]. Braidiant is intentionally
narrower: it does not attempt to solve pentagon equations, enumerate fusion
rings, or reproduce a full compiler or simulator. Instead, its primary unit
of work is a user-supplied F/R table and an independent, auditable numerical
verification report. This separation is useful for checking data from
multiple sources and for regression testing conventions before more
expensive simulations.

The distinction is one of workflow and auditability, not a demonstrated
performance advantage. No controlled speed or functionality superiority
benchmark against Anyonica, TQSim, or other packages is claimed in this
initial release. Interoperability with the larger fusion-category ecosystem
remains a future development opportunity rather than an implemented feature.

# Software design

Braidiant separates four mathematical concerns. A validated model object
stores finite charges, fusion channels, and complete complex-valued F/R
tables. A fusion-tree module enumerates basis states indexed by the sets of
leaf identities, which makes it possible to compare two different tree
parenthesizations or leaf orderings without confusing charges with positions.
Elementary rotations implement F matrices; local exchanges implement R
coefficients. Coherence tests are then expressed as comparisons between
composed paths through the same source and destination fusion spaces. For a
finite model, the code checks every admissible external and total charge
sector, and the output reports the largest absolute matrix-entry residual.

The braid representation module uses a separate graph search through binary
tree rotations to place adjacent anyons in a common fusion vertex. It
conjugates the local R action back to the reference left-associated basis,
then checks unitary normalization, the Yang–Baxter relation, and distant
commutation. This architecture is deliberately redundant: the numerical
coherence audit and the braid relation checks use different collections of
diagrams, providing a useful regression cross-check. A gauge-transformation
module exposes the dependence of individual symbols on vertex-basis phases,
while tests verify that coherence is retained and braid spectra are unchanged.

The trade-off is scale. Straightforward dense matrices and exhaustive sector
enumeration favor transparency and reproducibility on small and medium
reference models over large fusion spaces. Inputs with fusion multiplicities
greater than one, non-unitary structures, categorical pivotal data, mixed
external charges for braid representations, and experimental noise are not
supported. Numerical agreement within a tolerance is not an exact symbolic
proof of coherence.

# Research impact statement

The reference workflow reproduces expected Fibonacci and Ising fusion-space
dimensions, corresponding braid eigenphases, and numerical pentagon and
hexagon identities, with residuals at double-precision scale. Corrupted F
and R tables are deliberately included in regression tests and are rejected
by the appropriate diagnostics. The package also demonstrates consistency
under nontrivial unitary gauge rephasings and publishes the complete
reference calculation as executable code plus JSON output. These are
reproducible software-validation examples, **not claims of external adoption,
novel physics results, quantum-hardware measurements, or improved execution
speed**. This initial release has no demonstrated publication record or
external users. Research-impact evidence and a distributed record of public
development must be established before a JOSS submission; the current paper
is therefore a preparation draft and not an eligible immediate submission.

# AI usage disclosure

The initial software source, tests, documentation, release materials, and
this manuscript draft were prepared with assistance from **OpenAI ChatGPT
(GPT-6, November 2026)** for program architecture suggestions, code
implementation, test scaffolding, mathematical-expression checks, and
writing. The automated tests and reference examples were actually executed,
but this does **not** substitute for independent expert or human author
review. Before submission, the responsible human author must personally
review and validate the computational results and all AI-assisted text,
confirm the fundamental design decisions, edit the manuscript, and take
responsibility for the complete work. That confirmation is not claimed to
have occurred yet. This draft will be amended with a verified human
contribution statement before any journal submission.

# Acknowledgements

No external financial support is asserted for this initial code release.

# References
