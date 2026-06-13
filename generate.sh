#!/usr/bin/env bash
set -euo pipefail

mkdir -p cache build
wget -nv -N -c https://yaqwsx.github.io/jlcparts/data/cache.zip -P cache/

for i in $(seq -w 1 99); do
  url="https://yaqwsx.github.io/jlcparts/data/cache.z$i"
  wget -nv -N -c "$url" -P cache/ || break
done

7z x cache/cache.zip -ocache/ -aoa

python3 src/jlc_kicad_lib/main.py