# jlcpcb-to-kicad-sym

Generate a KiCad symbol library (`.kicad_sym`) from a list of JLCPCB/LCSC components while reusing stock KiCad footprints.

## What it does

- Reads a CSV of components keyed by `LCSC` part number.
- Maps each part to a stock KiCad footprint.
- Generates a KiCad symbol library in the modern s-expression `.kicad_sym` format.
- Writes common symbol fields such as `Value`, `Footprint`, `Datasheet`, `LCSC`, `Manufacturer`, and `MPN`.

## What it does not do

- It does not generate custom footprints.
- It does not guarantee a valid mapping for every JLCPCB/LCSC package.
- It does not yet fetch live catalog data; the first scaffold uses local sample data and mapping rules.

## Repository layout

```text
.
├── README.md
├── pyproject.toml
├── examples/
│   └── parts.csv
├── src/
│   └── jlc_kicad_lib/
│       ├── __init__.py
│       ├── cli.py
│       ├── generator.py
│       ├── footprints.py
│       ├── kicad_sym.py
│       └── models.py
└── tests/
    └── test_generator.py
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
jlc-kicad-lib generate examples/parts.csv --out output/JLC_Auto.kicad_sym --lib-name JLC_Auto
```
```
clear && pyenv shell 3.12.4 && python main.py
```
## Input format

The CSV should include these columns:

- `lcsc`
- `kind`
- `value`
- `package`
- `footprint`
- `description`
- `datasheet`
- `manufacturer`
- `mpn`

Example:

```csv
lcsc,kind,value,package,footprint,description,datasheet,manufacturer,mpn
C25804,resistor,10k,0603,Resistor_SMD:R_0603_1608Metric,Resistor 10k 1% 0603,https://example.com,UniOhm,0603WAF1002T5E
```

If `footprint` is blank, the tool will try to resolve it from `kind` and `package` using built-in mapping rules.

## Current scope

This scaffold supports a small first-pass set of atomic symbols:

- Resistors
- Capacitors
- Inductors
- LEDs

The next milestone should add:

1. Better package normalization.
2. Pin-map templates for diodes and transistors.
3. Optional live LCSC/JLCPCB enrichment.
4. Snapshot tests for generated `.kicad_sym` output.

## Development

Run tests:

```bash
pytest
```

Format and lint however you prefer. The code is intentionally small so you can replace the templates and mappings with your own policy.
