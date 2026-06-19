# jlcpcb-to-kicad-sym

Generate a KiCad symbol library (`.kicad_sym`) from a list of JLCPCB/LCSC components while reusing stock KiCad footprints.

## What it does

- Reads a SQLite DB of components keyed by `LCSC` part number.
- Maps each part to a stock KiCad footprint.
- Generates a KiCad symbol library in the modern s-expression `.kicad_sym` format.
- Writes common symbol fields such as `Value`, `Footprint`, `Datasheet`, `LCSC`, `Manufacturer`, and `MPN`.

## What it does not do

- It does not generate custom footprints.
- It does not guarantee a valid mapping for every JLCPCB/LCSC package.
- It does not fetch live catalog data; this project uses a cached BD from JLCPCB, likeley updated weekly, see [upstream](https://yaqwsx.github.io/jlcparts).

## Repository layout

```text
.
├── README.md
├── src/
│   ├── jlc_kicad_lib/
│   |   ├── __init__.py
│   |   ├── footprint_packages.py
│   |   ├── generator.py
│   |   ├── main.py
│   |   ├── patterns.py
│   |   └── symbols.py
|   └── kicad-library-utils
```

## Quick start

```bash
./generate.sh
```

## Input format

This script fetches the latest SQLite DB from https://yaqwsx.github.io/jlcparts and generates some basic libraries from it.

## Current scope

This scaffold supports a small first-pass set of atomic symbols:

- Resistors
- Capacitors
- Inductors
- LEDs

The next milestone should add:

1. Better package normalization.
2. Snapshot tests for generated `.kicad_sym` output.

## Development

Run tests:

```bash
```
