"""Command-line interface for verifiable model, braid and invariant calculations."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys

from .models import fibonacci, cyclic, ising
from .audit import audit
from .braid import BraidRepresentation, matrix_json
from .invariants import fusion_invariants, braiding_invariants
from .io import load_model, model_to_dict
from .model import ModelError


def model_fingerprint(model) -> str:
    """SHA-256 of canonical JSON, including the declared symbol gauge."""
    canonical = json.dumps(model_to_dict(model), sort_keys=True,
                           separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="bradiant", description="Numerical anyon diagnostics")
    parser.add_argument("--model", choices=["fibonacci", "ising", "cyclic"], default="fibonacci")
    parser.add_argument("--model-file", help="JSON model file, overrides --model and --n")
    parser.add_argument("--n", type=int, default=3, help="Z_n order for cyclic model")
    parser.add_argument("--k", type=int, default=1, help="bicharacter coefficient for Z_n")
    parser.add_argument("--output", default="-", help="JSON output filename, or '-' for stdout")
    parser.add_argument("--tol", type=float, default=1e-10)
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("audit", help="verify every pentagon, hexagon and tensor-unit sector")
    subs.add_parser("invariants", help="calculate fusion dimensions and gauge-invariant monodromy")
    braid = subs.add_parser("braid", help="construct braid generators and optional word")
    braid.add_argument("--charge", default="tau")
    braid.add_argument("--anyons", type=int, default=4)
    braid.add_argument("--total", default="1")
    braid.add_argument("--word", default="", help="comma-separated signed braid indices, e.g. 1,-2,1")
    args = parser.parse_args(argv)
    try:
        if not (0 < args.tol < float('inf')):
            raise ValueError("tol must be finite and positive")
        model = (load_model(args.model_file) if args.model_file else
                 ({"fibonacci": fibonacci, "ising": ising}.get(
                     args.model, lambda: cyclic(args.n, args.k))()))
        check = audit(model, tol=args.tol)
        payload = {"schema_version": 1, "model": model.name,
                   "model_sha256": model_fingerprint(model),
                   "type": {"audit":"model_audit", "braid":"braid_representation"}.get(
                       args.command, args.command)}
        if args.command == "audit":
            payload.update(check.to_dict())
            status = 0 if check.passed else 1
        elif args.command == "invariants":
            payload.update({"audit": check.to_dict(),
                            "fusion": fusion_invariants(model).to_dict(),
                            "braiding": braiding_invariants(model, tol=args.tol).to_dict()})
            status = 0 if check.passed else 1
        else:
            if not check.passed:
                raise ModelError("model fails the numerical coherence audit; braid operation refused")
            rep = BraidRepresentation(model, args.charge, args.anyons, args.total)
            word = [int(x.strip()) for x in args.word.split(",") if x.strip()]
            payload.update({"charge": rep.charge, "anyons": rep.number, "total": rep.total,
                            "dimension": rep.dimension, "word": word,
                            "word_matrix": matrix_json(rep.word(word)),
                            "relations": rep.relations(),
                            "generators": {str(i): matrix_json(rep.generator(i))
                                           for i in range(1, rep.number)}})
            status = 0 if max(payload["relations"].values()) <= args.tol else 1
        blob = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.output == "-":
            sys.stdout.write(blob)
        else:
            with open(args.output, "w", encoding="utf-8") as output:
                output.write(blob)
        return status
    except (ValueError, KeyError, ModelError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    sys.exit(main())
