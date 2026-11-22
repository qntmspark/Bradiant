"""Portable, explicit model file schema. No executable deserialization."""
from __future__ import annotations
import json
from pathlib import Path
from .model import FusionModel, ModelError


def model_to_dict(model: FusionModel) -> dict:
    """Stable JSON model representation with canonical sorted table rows."""
    return {
        "schema_version": 1,
        "name": model.name,
        "unit": model.unit,
        "charges": list(model.charges),
        "fusion": [[a,b,list(outputs)] for (a,b),outputs in sorted(model.fusion.items())],
        "F": [[*k, float(v.real), float(v.imag)]
              for k,v in sorted(model.f_symbols.items())],
        "R": [[*k, float(v.real), float(v.imag)]
              for k,v in sorted(model.r_symbols.items())],
    }


def model_from_dict(data: dict) -> FusionModel:
    """Load validated multiplicity-free model; reject missing and duplicate entries."""
    if data.get("schema_version") != 1:
        raise ModelError("unsupported schema_version")
    charges = tuple(data["charges"])
    fusion = {}
    for row in data["fusion"]:
        if len(row) != 3 or tuple(row[:2]) in fusion:
            raise ModelError("invalid/duplicate fusion entry")
        fusion[tuple(row[:2])] = tuple(row[2])
    F = {}
    for row in data["F"]:
        if len(row) != 8 or tuple(row[:6]) in F:
            raise ModelError("invalid/duplicate F entry")
        F[tuple(row[:6])] = complex(row[6],row[7])
    R = {}
    for row in data["R"]:
        if len(row) != 5 or tuple(row[:3]) in R:
            raise ModelError("invalid/duplicate R entry")
        R[tuple(row[:3])] = complex(row[3],row[4])
    return FusionModel(str(data["name"]), charges, data["unit"], fusion, F, R)


def save_model(model: FusionModel, filename: str | Path) -> None:
    Path(filename).write_text(json.dumps(model_to_dict(model), indent=2, sort_keys=True) + "\n",
                              encoding="utf-8")


def load_model(filename: str | Path) -> FusionModel:
    return model_from_dict(json.loads(Path(filename).read_text(encoding="utf-8")))
