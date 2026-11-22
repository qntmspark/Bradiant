# JOSS manuscript formatting and source of truth

The article is authored in `paper.md`, with its BibTeX references in `paper.bib`.
The published *The Walrus* JOSS article (https://doi.org/10.21105/joss.01705)
was used as a visual reference for restrained scientific prose, the JOSS masthead,
author/affiliation block, body typography, citations, sidebar, and footer.
The 2019 manuscript does **not** supersede current JOSS paper requirements.

## Current JOSS structure

The document uses Pandoc/YAML metadata and the currently required sections:
Summary, Statement of need, State of the field, Software design, Research
impact statement, AI usage disclosure, Acknowledgements, and References.
The body is about 975 words, within JOSS's 750–1,750-word range.

## Official typesetting

`.github/workflows/draft-pdf.yml` calls
`openjournals/openjournals-draft-action@master` on changes to the manuscript,
its references, or the workflow. The resulting `paper.pdf` is saved as the
`bradiant-joss-draft` artifact on the GitHub Actions run.

The reference build on 2026-11-22 passed:
https://github.com/qntmspark/Bradiant/actions/runs/44978346689

The official proof is watermarked **DRAFT**, contains line numbers and a
placeholder `10.xxxxxx/draft` DOI, and may display journal/editor/date
placeholders. None of those fields constitutes a real review, submission,
publication, or assigned DOI. They should **not** be copied into citation
metadata or user-facing claims. The accepted paper's sidebar information is
inserted by the journal during the editorial process.

## Remaining items

The human author must verify and replace the current author/affiliation
placeholders. Independent human scientific validation, public-development
history, outside research-use evidence, and an archival DOI are still pending
(see `docs/joss_readiness.md`).

Sources: https://joss.readthedocs.io/en/latest/paper.html and
https://joss.readthedocs.io/en/latest/submitting.html
