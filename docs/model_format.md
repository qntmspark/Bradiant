# External model JSON schema (v1)

Braidiant does not execute code from model files. Load using
`braidiant.load_model("path.json")` or the CLI `--model-file path.json`.

Top-level required fields:

- `schema_version`: integer `1`
- `name`: arbitrary display string
- `unit`: charge label as a string
- `charges`: unique list of charge label strings, defining stable ordering
- `fusion`: one `[a, b, [c, ...]]` row for every ordered pair `a,b`
- `F`: every allowed `[a, b, c, d, e, f, real, imaginary]` row
- `R`: every allowed `[a, b, c, real, imaginary]` row

A complete Fibonacci example is located at `examples/fibonacci.json`. Zero F
entries inside an otherwise admissible block **must be included**. Missing
entries and duplicates are rejected. The format makes no unspoken assumption
that singleton F-symbols equal one, and no attempt is made to infer gauge from
partial data.

All real and imaginary values are finite JSON numbers. Symbols with magnitudes
or coherence residuals outside tolerance cause an audit failure, not an
unreported repair of the input data.

Input example using the API:

```python
from braidiant import fibonacci, save_model, load_model, regauge, audit
import cmath
m = fibonacci()
rephased = regauge(m, {("tau", "tau", "tau"): cmath.exp(0.3j)})
save_model(rephased, "rephased.json")
assert audit(load_model("rephased.json")).passed
```
