"""Deterministic scientific benchmarks; produces checked example evidence.

Usage: python examples/reproduce.py > examples/reference_results.json
Records numerical residuals, not a physical experiment or speedup claim.
"""
import json
from braidiant import audit, fibonacci, ising, cyclic, BraidRepresentation

models = [fibonacci(), ising(), cyclic(3)]
output = {"schema_version": 1, "note": "double-precision numerical verification only",
          "model_audits": [audit(m).to_dict() for m in models], "braid_examples": []}
for m, charge, n, total in [(fibonacci(), "tau", 4, "1"),
                            (fibonacci(), "tau", 6, "1"),
                            (ising(), "sigma", 4, "1"),
                            (ising(), "sigma", 6, "1")]:
    rep = BraidRepresentation(m, charge, n, total)
    output["braid_examples"].append({"model": m.name, "charge": charge, "n": n,
                                     "total": total, "dimension": rep.dimension,
                                     "relations": rep.relations()})
print(json.dumps(output, indent=2, sort_keys=True))
