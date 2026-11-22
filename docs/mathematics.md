# Mathematical contract and numerical methods

## 1. The data model

A *multiplicity-free* fusion rule has integers `N[a,b,c]` equal to 0 or 1.
Fusion is therefore represented as ordered lists of permitted output charges.
All modules use explicit charge labels and require a two-sided tensor unit.
If a model's fusion rules are associative, then for each `a,b,c,d` the two
fusion-channel sets

\[
E = \{e : N_{ab}^{e} N_{ec}^{d}=1\},\qquad
T = \{f : N_{bc}^{f} N_{af}^{d}=1\}
\]

have equal cardinality. Inputs with unequal sizes are rejected. The order of
these sets is derived from the order of `charges` and each charge-pair's
`fusion` row. Models must explicitly supply the complete F and R tables.

## 2. F- and R-symbol conventions

The F matrix changes between left and right associated fusion trees:

\[
|((ab)_e c)_d\rangle = \sum_f (F_d^{abc})_{ef}
|(a (bc)_f)_d\rangle.
\]

Code acting on a **column vector** in the left basis uses
`M[target_f, source_e] = F[e,f]`. Reverse rotations use its complex conjugate
transpose, which is justified only for unitary F matrices. Unitary F-block
checks are part of the audit; malformed F data may produce failing diagnostics
instead of a valid inverse.

An R symbol applies to an exchange at a common fusion vertex,
`(a,b)->(b,a)`, in the channel `c`. In this representation, clockwise-positive
is a **defined mathematical sign convention**; physically assigning that sign
to a laboratory exchange requires a choice of planar orientation.

## 3. Graphical coherence by explicit path composition

A fusion tree is a nested pair of integer-indexed leaves. Internal basis
channels are keyed by the corresponding *set of leaf identities*, which
remains well-defined even when local braidings permute their order. Each
F move and R move is implemented as a finite matrix between complete fusion
bases. Five 4-leaf trees are used for the pentagon:

```
T0 = (((ab)c)d)       T1 = ((a(bc))d)
T2 = (a((bc)d))       T3 = (a(b(cd)))
T4 = ((ab)(cd))
```

The checked identity compares `T0 -> T1 -> T2 -> T3` against
`T0 -> T4 -> T3` for every four external charges and every total charge.

For the first hexagon, compare the direct subtree exchange
`(a(bc)) -> ((bc)a)` against the five elementary maps

```
(a(bc)) -> ((ab)c) -> ((ba)c) -> (b(ac)) -> (b(ca)) -> ((bc)a)
```

For the second hexagon, compare `((ab)c) -> (c(ab))` against

```
((ab)c) -> (a(bc)) -> (a(cb)) -> ((ac)b) -> ((ca)b) -> (c(ab))
```

Both sides are matrices with the same ordered source/target fusion bases.
The reported residual is their largest absolute entrywise complex
difference. The value is evaluated for **every** admissible total sector.

## 4. Gauge transformations

Rephase each splitting/fusion vertex by `g[a,b,c]`, a unit complex number.
Our convention transforms symbols as

\[
F'^{abc}_{d;ef} =
\frac{g_{ab}^{e}g_{ec}^{d}}{g_{bc}^{f}g_{af}^{d}} F^{abc}_{d;ef},
\qquad
R'^{ab}_c=\frac{g_{ab}^{c}}{g_{ba}^{c}}R^{ab}_c.
\]

Vertices involving the tensor unit are gauge fixed to 1. The code includes
nontrivial gauge-rotation regression tests for Fibonacci and Z3 data.
Gauge changes modify matrix elements but not the physical braid spectra.

## 5. Braid generators

Given n identical external charges, we choose the left-associated fusion
basis, fixed total charge, and enumerate all permitted internal labels. To
produce the generator sigma_i, we search the finite graph of binary-tree
rotations for a tree where leaves i and i+1 are siblings. If U maps from
the reference tree to that local tree, then

\[
\rho(\sigma_i) = U^\dagger \mathrm{diag}(R^{aa}_{c}) U.
\]

This builds explicit matrices without hard-coding position-specific formulas.
The auditor checks `sigma_i sigma_(i+1) sigma_i = sigma_(i+1) sigma_i
sigma_(i+1)` and `sigma_i sigma_j = sigma_j sigma_i` for `|i-j|>1`, as
well as unitary normalization. Braid words multiply in the order their
generators are applied; a negative letter is the matrix inverse.

## 6. Scope of numerical claims

- All arithmetic is double-precision complex and uses NumPy.
- "Exhaustive" means **all finite charge sectors of the input model**, not
  an infinite theoretical proof, and not a search across all possible models.
- Residuals are numerical diagnostics, not exact equality proofs. The
  default acceptance tolerance is 1e-10 and can be changed by the caller.
- The braid algorithm has exponentially growing fusion spaces and Catalan
  tree-search complexity, so the CLI currently limits n to at most 9.
- Unsupported: fusion multiplicities >1; non-unitary F-symbols; non-semisimple
  categories; nontrivial pivotal structures; evaluation of topological spins,
  S matrices, ribbon twists and modularity proofs; mixed-charge braiding; experimental noise models.
- No numerical accelerator, circuit synthesis compiler or certified interval
  arithmetic is claimed.

## 7. References and cross-checks

The implemented graphical identities and conventions align with standard
accounts in Preskill's *Topological Quantum Computation* lecture notes, and
Pachos' *Introduction to Topological Quantum Computation*. Test cases include
Fibonacci, chiral Ising and pointed cyclic models. Known reference braid
spectra and Fibonacci/Ising fusion-space dimensions are tested directly.
The exact source bibliography is in `paper.bib`.

## 8. Fusion and braiding invariants

For each simple object `a`, define the integer fusion matrix
`(N_a)_{bc} = N_{ab}^c`. The vector of Frobenius--Perron dimensions is
the positive common eigenvector

\[
\sum_c N_{ab}^{c} d_c = d_a d_b, \qquad d_{\mathbf{1}}=1.
\]

The implementation numerically finds the dominant eigenvector of
`M = sum_a N_a`, normalizes its vacuum entry to one, and independently
checks every `N_a d = d_a d`. It reports the residual, the squared global
dimension `Dim = sum_a d_a^2`, and total dimension `sqrt(Dim)`. In a
**unitary fusion category** the FP dimensions agree with the canonical
positive quantum dimensions. These cannot in general be equated for arbitrary
nonunitary input.

The gauge-independent channel double braiding is

\[
M_{ab}^{c} = R_{ab}^{c} R_{ba}^{c}.
\]

An object is transparent if `M_ab^c=1` in every allowed channel for every
`b`, within the specified numerical tolerance. The outputs characterize the
transparent part of a coherent braided fusion system; they do not provide
ribbon twists, S matrices, topological central charge, or a proof of
non-degeneracy. A `cyclic(4,1)` model has a nontrivial transparent object
`2`, while Fibonacci and chiral Ising have only the unit as transparent.

## 9. Tensor-unit normalization and precise failure reports

We fix a strict unit gauge. Whenever one external input in an F move is the
tensor unit, the corresponding F matrix should be the identity, and exchanging
the unit with any charge gives R=1. The audit separately reports the maximum
`unit_residual`. For pentagon/hexagon residuals, `worst_*_sector` records the
external charge labels and total charge at the largest error. These fields
help isolate inconsistencies without mistaking a scalar global maximum for a
complete diagnosis of a custom model.
