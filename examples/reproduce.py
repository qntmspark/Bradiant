"""Generate reproducible *numerical* reference evidence (not hardware data)."""
import json
import sys
from bradiant import (audit, fibonacci, ising, cyclic, BraidRepresentation,
                       fusion_invariants, braiding_invariants, __version__)
import numpy as np

models = [fibonacci(), ising(), cyclic(3), cyclic(4)]
output = {
    "schema_version": 2,
    "bradiant_version": __version__,
    "numpy_version": np.__version__,
    "python_version": sys.version.split()[0],
    "evidence_type": "double_precision_numerical_consistency_checks_not_hardware",
    "models": [],
    "braid_examples": []
}
for model in models:
    output["models"].append({
        "name": model.name,
        "audit": audit(model).to_dict(),
        "fusion": fusion_invariants(model).to_dict(),
        "braiding": braiding_invariants(model).to_dict()
    })
for model, charge, n, total in [
    (fibonacci(), "tau", 4, "1"), (fibonacci(), "tau", 6, "1"),
    (ising(), "sigma", 4, "1"), (ising(), "sigma", 6, "1")
]:
    rep = BraidRepresentation(model, charge, n, total)
    output["braid_examples"].append({
        "model": model.name, "charge": charge, "n": n,
        "total": total, "dimension": rep.dimension,
        "relations": rep.relations()
    })
print(json.dumps(output, indent=2, sort_keys=True))
