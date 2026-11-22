# JOSS submission packet (draft, not yet eligible)

This is a set of truthful draft answers for the JOSS web form. Do not submit
before the editorial eligibility conditions in `joss_readiness.md` are met.

- **Software title:** Braidiant: Reproducible numerical audits of anyon fusion and braiding data
- **Software repository:** https://github.com/qntmspark/QuantumSparkNew/tree/braidiant-oss
  (temporary public branch; a dedicated repository is required for clean maintenance)
- **Paper:** `paper.md` in the same branch
- **Bibliography:** `paper/references.bib`
- **License:** MIT, full license included in `LICENSE`
- **Language:** Python (NumPy dependency)
- **Keywords:** topological quantum computation; anyons; fusion categories;
  pentagon and hexagon coherence; numerical validation; braid groups
- **Description:** A Python implementation for exhaustive numerical audits of
  finite multiplicity-free unitary braided fusion data. It verifies
  associator/braiding consistency, constructs braid-group matrices, and
  evaluates gauge-invariant diagnostics with reproducible JSON records.
- **Target users:** mathematical physicists, quantum information researchers,
  computational topologists, developers validating F/R tables.
- **Existing software:** Anyonica, TensorCategories.jl, TQSim.
- **Potential research application:** validating an externally sourced
  F/R dataset before consuming it in an anyonic simulation workflow.
- **Available evidence:** executable reference models, 58 locally executed
  automated tests (as of this draft), source-independent expected values,
  corruption detection, and a local timing protocol. This is **not** evidence
  of independent external research adoption.
- **Publication/archival DOI:** none assigned; do not fabricate a DOI.
- **Author and affiliation:** *human author must verify and enter their own
  correct identity and appropriate affiliation*. GitHub username is not a
  substitute for an accurate author record.
- **AI use:** JOSS requires disclosure; the draft paper includes a truthful
  statement and notes that human validation has not yet been confirmed.
- **Previous submissions:** none claimed.

## Before submission

1. Maintain an actual, public, iterative development history for more than six
   months, with descriptive commits, issues, releases and reviews. Do not
   backdate commits or create simulated community engagement.
2. Demonstrate actual research use by developers, preferably also external
   researchers, with independent reproduction and public evidence.
3. Arrange review by a human who understands fusion-category conventions;
   resolve their concrete code and manuscript findings.
4. Create a dedicated open repository and confirm issues/PRs, LICENSE, tests,
   docs and installation work for a third party.
5. Verify the manuscript author, affiliations, relevant ethics/disclosures,
   all bibliography details, and human responsibility statement.
6. Create an archived software release/DOI (e.g. Zenodo) when the maintained
   repository and release are stable; update paper and `CITATION.cff`.
7. Validate `paper.md` with the official JOSS paper build before filling the
   form at https://joss.theoj.org/papers/new.

JOSS sources checked 2026-11-21:
https://joss.readthedocs.io/en/latest/submitting.html
https://joss.readthedocs.io/en/latest/paper.html
https://joss.readthedocs.io/en/latest/review_criteria.html
https://joss.readthedocs.io/en/latest/policies.html
