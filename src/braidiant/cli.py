"""Command line reproducibility interface."""
import argparse
import json
import sys
from .models import fibonacci, cyclic, ising
from .audit import audit
from .braid import BraidRepresentation, matrix_json
from .io import load_model


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="braidiant", description="Anyons: audit, represent, reproduce")
    parser.add_argument("--model", choices=["fibonacci", "ising", "cyclic"], default="fibonacci")
    parser.add_argument("--model-file", help="JSON model file, overrides --model and --n")
    parser.add_argument("--n", type=int, default=3, help="Z_n order for cyclic model")
    parser.add_argument("--k", type=int, default=1, help="bicharacter coefficient for Z_n")
    parser.add_argument("--output", default="-", help="JSON output filename, or '-' for stdout")
    parser.add_argument("--tol", type=float, default=1e-10)
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("audit", help="enumerate every pentagon and hexagon sector")
    braid = subs.add_parser("braid", help="construct braid generators and optional word")
    braid.add_argument("--charge", default="tau")
    braid.add_argument("--anyons", type=int, default=4)
    braid.add_argument("--total", default="1")
    braid.add_argument("--word", default="", help="comma-separated signed braid indices, e.g. 1,-2,1")
    args = parser.parse_args(argv)
    model = (load_model(args.model_file) if args.model_file else
             ({"fibonacci": fibonacci, "ising": ising}.get(args.model, lambda: cyclic(args.n, args.k))()))
    try:
        if args.command == "audit":
            result = audit(model, tol=args.tol)
            payload = {"schema_version": 1, "type": "model_audit", **result.to_dict()}
            status = 0 if result.passed else 1
        else:
            rep = BraidRepresentation(model, args.charge, args.anyons, args.total)
            word = [int(x.strip()) for x in args.word.split(",") if x.strip()]
            payload = {"schema_version": 1, "type": "braid_representation", "model": model.name,
                       "charge": rep.charge, "anyons": rep.number, "total": rep.total,
                       "dimension": rep.dimension, "word": word,
                       "word_matrix": matrix_json(rep.word(word)),
                       "relations": rep.relations(),
                       "generators": {str(i): matrix_json(rep.generator(i))
                                      for i in range(1, rep.number)}}
            status = 0 if max(payload["relations"].values()) <= args.tol else 1
        blob = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.output == "-":
            sys.stdout.write(blob)
        else:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(blob)
        return status
    except (ValueError, KeyError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    sys.exit(main())
