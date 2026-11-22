"""Reproducible, machine-local timing protocol; no third-party comparisons.

Run: python examples/benchmark.py --repeats 7 > benchmark.json
The times are environment-dependent descriptive measurements, not performance claims.
"""
import argparse
import json
import platform
import statistics
import time
import numpy as np
from bradiant import audit, fibonacci, ising, cyclic, BraidRepresentation


def time_task(action, repeats):
    # One untimed warm-up; measure full call with fresh object/return value.
    action()
    durations = []
    for _ in range(repeats):
        start = time.perf_counter()
        action()
        durations.append(time.perf_counter() - start)
    return {"median_seconds": statistics.median(durations),
            "min_seconds": min(durations), "max_seconds": max(durations),
            "repeats": repeats}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=7)
    args = parser.parse_args()
    if args.repeats < 3:
        parser.error("repeats must be >=3")
    tasks = {
        "audit_fibonacci": lambda: audit(fibonacci()),
        "audit_ising": lambda: audit(ising()),
        "audit_z3": lambda: audit(cyclic(3)),
        "braid_fibonacci_6": lambda: BraidRepresentation(fibonacci(), "tau", 6, "1").relations(),
        "braid_ising_6": lambda: BraidRepresentation(ising(), "sigma", 6, "1").relations(),
    }
    out = {"benchmark_protocol": "perf_counter warmup once, repeated full calls",
           "python": platform.python_version(), "platform": platform.platform(),
           "numpy": np.__version__, "timings": {}}
    for name, action in tasks.items():
        out["timings"][name] = time_task(action, args.repeats)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
