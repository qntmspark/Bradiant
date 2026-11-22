# JOSS preparation checklist

**Current stage: open-source candidate with completed local QA, not eligible for
immediate JOSS submission.** This file does not claim the paper was submitted,
peer-reviewed or accepted.

The JOSS rules reviewed on 2026-11-21 require a public repository with more
than six months of *active, distributed development*, evidence of genuine
research use, significant software contribution, usable documentation/tests,
open development workflows, and an AI-use statement with human validation.
A newly uploaded code dump does not meet the public-history requirement.

## Software requirements

- [x] Open-source license (MIT) included.
- [x] Installable Python package and `pyproject.toml`.
- [x] Runnable tests including independent positive and negative checks.
- [x] JSON model interchange, CLI and stable examples.
- [x] Documentation of mathematics, limitations and reproducibility.
- [x] GitHub Actions CI workflow supplied; new main-branch run must pass.
- [x] JOSS-formatted **draft** `paper.md` with canonical root `paper.bib`.
- [x] Official Open Journals PDF generator succeeded (2026-11-22): https://github.com/qntmspark/Bradiant/actions/runs/44982374465.
- [x] Full document visually checked after journal typesetting (three-page draft).
- [x] Gauge-independent dimensions and double-braiding invariants, analytic checks.
- [x] Reproducible local timing protocol and full source distribution.
- [ ] Independent scientific cross-validation and external feedback.
- [ ] Stable public upstream repository with full issue tracker and reviewable PRs.
- [ ] >6 months of active public development with releases distributed in time.
- [ ] Recorded research use in a preprint, research workflow, or external project.
- [x] Manuscript author identity and independent-researcher affiliation confirmed.
- [ ] Human author verifies contribution statements,
      mathematical and programming choices, software claims, licensing and AI disclosure.
- [ ] Permanent archived software release (e.g., Zenodo) with real DOI; JOSS draft DOI is an automated placeholder, not a DOI.
- [ ] JOSS form submitted and editorial pre-review issue opened.

## Sustainable development plan

Version 0.1: numerical audit, reference models, source release, initial
reproducibility results. Version 0.2: stronger structural/unit validation,
channel-wise monodromy, Perron--Frobenius invariants, provenance hashes,
analytic cross-checks and reproducible timing protocol. Future iterations should be driven by actual use and
public issue reports. Potential research extensions include efficient fusion
basis enumeration, category datasets with explicit gauge provenance,
interop with AnyonWiki, mixed-charge braid groupoids, precision/interval
certification, and independent comparisons with existing software.
No roadmap item should be described as implemented before it has been tested.

## Integrity

JOSS requires disclosure of AI-assisted code and writing, including the tools
and versions used and evidence of human validation; AI-assisted conversational
responses to editors/reviewers are restricted. The draft states actual AI
assistance and deliberately **does not pretend the human sign-off has happened**.

Sources: https://joss.readthedocs.io/en/latest/submitting.html
and https://joss.readthedocs.io/en/latest/paper.html
