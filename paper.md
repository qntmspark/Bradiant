---
title: 'Braidiant: Reproducible numerical audits of anyon fusion and braiding data'
tags:
  - Python
  - topological quantum computation
  - fusion categories
  - anyons
  - braid groups
  - numerical verification
authors:
  - name: 'AUTHOR NAME TO VERIFY BEFORE SUBMISSION'
    affiliation: '1'
affiliations:
  - name: 'Independent researcher, United States (confirm affiliation before submission)'
    index: 1
date: 21 November 2026
bibliography: paper/references.bib
---

# Summary

Non-Abelian anyons are quasiparticle excitations whose exchanges act as
operations on a shared quantum state space. Their mathematical descriptions
use *fusion rules*, which specify possible results of combining excitations,
and two types of complex-valued coefficients: **F symbols**, governing changes
in the grouping of fusion operations, and **R symbols**, governing exchanges.
A table of coefficients can look plausible while violating the fundamental
consistency requirements that make distinct sequences of regroupings and
exchanges describe the same physical process. Detecting such errors is
important before inserting category data into larger numerical calculations.

**Braidiant** is a Python research package for inspecting these data. It
accepts finite, multiplicity-free fusion rules together with explicit
numerical F and R tables; exhaustively evaluates the pentagon and both
hexagon identities across their admissible charge sectors; and constructs
finite-dimensional braid-group matrices in reproducibly ordered fusion-path
bases. Additional checks cover tensor-unit normalization, unitarity,
Frobenius--Perron dimensions, double-braiding phases, and transparent
objects. The package provides validated JSON interchange, machine-readable
residuals, a command-line interface, a Python API, reference models, and
executable verification experiments.

# Statement of need

Topological quantum computation relies on nonlocal state spaces and
representations of particle exchanges [@nayak2008; @pachos2012]. Category data
are increasingly relevant to software workflows exploring braiding,
topological phases, and quantum information. Fusion outcomes alone are not
sufficient to establish a consistent braided model: associators and exchange
coefficients must satisfy pentagon and hexagon coherence, respectively.
Numerical evaluation presents additional pitfalls: a missing allowed F entry,
ambiguous basis ordering, misplaced complex conjugation, or inconsistent
vertex gauge can compromise results while producing unitary-looking matrices.

Braidiant addresses the practical need for a small, inspectable **verification
boundary** between the source of numerical category tables and software that
consumes them. The target audience includes researchers and students working
with fusion categories, anyonic quantum algorithms, and numerical topological
models. A deterministic data schema preserves all allowed F entries,
including zeros; numerical tests report failures rather than silently
reconstructing missing information. Sector-specific maxima identify charges
responsible for pentagon and hexagon discrepancies, while model fingerprints
connect reported calculations to the precise table and gauge submitted.

# State of the field

Existing software has overlapping and often broader capabilities. **Anyonica**
implements symbolic methods for obtaining and manipulating fusion-category
data and has supported systematic investigations of low-rank multiplicity-free
categories [@vercleyen2026]. **TensorCategories.jl** offers a general
computational algebra framework for tensor categories, including exact and
numerical skeletal fusion data and coherence checks [@tensorcategories2026].
**TQSim** simulates topological quantum circuits based on Fibonacci anyons
[@tqsim]. These packages establish that Braidiant is not the first tool to
compute coherence identities or braid matrices.

The design case for a separate implementation is intentionally specific:
Braidiant exposes a lightweight Python-only, table-first audit interface,
uses an explicit portable JSON representation, reports failure-sector
information and gauge-invariant diagnostics, and generates basis-dependent
braid matrices without a full category solver or anyonic circuit runtime.
These choices support cross-checking a dataset produced elsewhere before
using it in Python analyses. They do **not** establish superior generality,
speed, or algorithmic novelty relative to existing category software.
A future interoperability comparison is an important part of establishing
this package's independent research impact.

# Software design

The implementation separates structural input validation from numerical
coherence, representation construction, and gauge-independent invariants.
The model layer requires a two-sided tensor unit, rigid duals, complete
fusion tables, allowed F/R entries, and valid channel dimensions. It rejects
unused symbols rather than allowing unchecked data to appear validated.
A common fusion-tree algebra maps elementary recouplings and exchanges
between explicitly enumerated finite bases. The audit composes two different
paths through each coherence diagram, comparing full complex matrices for
all admissible external and total charges. Reporting the largest entrywise
residual per family makes numerical tolerances directly inspectable.

For braids, breadth-first search over binary-tree rotations locates a tree
in which the two relevant particles fuse locally. Conjugating the diagonal
R-symbol exchange by the recoupling map returns a generator to a common
left-associated basis. Braid generators can then be checked against the
Yang--Baxter and distant-commutation relations. Independently, fusion
matrices yield the common positive eigenvector defining Frobenius--Perron
dimensions, while channel monodromies are evaluated as products of the two
oppositely ordered R symbols. The modularity-related transparent-object
test uses those gauge-invariant monodromies without inferring a ribbon
structure or an S matrix from insufficient data.

The design favors clarity and independently inspectable small models over
asymptotic efficiency. Dense matrices, exhaustive charge-sector enumeration,
and tree searches scale poorly to large fusion spaces. The implementation
currently assumes finite, unitary, multiplicity-free input and homogeneous
external charges for braid representations. It neither solves the
coherence equations nor produces formal certificates, mixed-charge braid
groupoids, noise models, or hardware predictions. Such distinctions matter:
a small residual at double precision is evidence of numerical consistency,
not a proof of categorical coherence.

# Research impact statement

The repository includes source-independent analytic checks as well as
executable numerical evidence. The reference calculation evaluates 27
pentagon and 24 hexagon charge sectors for Fibonacci data, and 106 pentagon
and 66 hexagon sectors for the chiral Ising model. Their maximum hexagon
residuals are approximately $3.14\times10^{-16}$ and
$3.41\times10^{-16}$, respectively, under the declared double-precision
conventions. Further tests recover the Fibonacci dimension
$(1+\sqrt{5})/2$ and Ising charge dimension $\sqrt{2}$, reproduce known
monodromy phases, and identify a nontrivial transparent object in a pointed
$\mathbb{Z}_4$ example. Deliberately corrupted F/R data and randomly
rephased gauges exercise both failure detection and invariance. The
reference JSON data and environment-local timing protocol can be regenerated
from versioned scripts, and automated tests exercise the package API and CLI.

These results document **research-workflow capability and numerical software
verification**, not a novel physical result. No independent external users,
research publications using the package, hardware tests, or comparative
speedups have been demonstrated as of this draft. Sustained public
open-source development and evidence of scientific use remain necessary
before this manuscript can satisfy JOSS pre-review eligibility criteria.

# AI usage disclosure

OpenAI ChatGPT (GPT-6, November 2026) assisted with software architecture,
Python implementation, tests, documentation, numerical verification design,
and drafting/editing this manuscript. The numerical reference calculations
and automated tests were executed, including analytic reference comparisons,
input-corruption tests, and gauge checks. These computational tests are not
independent human scientific validation. Before submission, the responsible
human author must review and modify the assisted work, validate the
mathematical and software claims, take responsibility for the design, and
confirm this assessment accurately. That human verification is **pending**;
it is not represented here as already complete.

# Acknowledgements

No external financial support has been claimed for this release.

# References
