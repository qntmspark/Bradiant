# Contributing to Bradiant

We welcome bug reports, independent verification, models with published source
conventions, and focused, test-backed additions.

1. Open an issue describing the scientific use case, expected behavior and
   exact source for any F/R symbol table.
2. Fork the repository and create a descriptive branch; do not force-push to
   other people's review branches.
3. Install with `pip install -e '.[dev]'` and run `pytest` before submitting.
4. Add positive and negative tests, document any numerical tolerances, and
   update reproducibility fixtures when outputs change.
5. Create a pull request describing mathematical conventions, provenance,
   limitations and expected runtime scaling.

The maintainers will review correctness and contribution rights before
acceptance; an issue/PR does not imply endorsement or acceptance.

## Scientific integrity and security

Do not include unsupported hardware claims, invented benchmark improvements,
secrets, private data, copyright-infringing reference tables or misleading
claims of exact proof. Report security issues privately to the repository
maintainer rather than publishing exploitation details in an issue.

## Governance and support

This is initially a small maintainer-led project. Changes to the mathematical
contract or public data format require a documented proposal and regression
suite. GitHub issues are the supported help and bug-report channel. No
commercial support, service-level guarantee, or indefinite maintenance is
promised. Project contributors retain authorship of their contributions.
