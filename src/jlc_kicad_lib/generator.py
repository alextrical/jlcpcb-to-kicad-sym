import re
import sqlite3
import sys

sys.path.append("src/kicad-library-utils/common")
import kicad_sym

from kicad_sym import KicadLibrary, KicadSymbol, Property
from patterns import PATTERNS
from pathlib import Path

def create_connection(db_path: str):
    return sqlite3.connect(db_path)

OUTPUT_DIR = Path("build")

def create_library(libname: str, output_dir: Path = OUTPUT_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)
    library_path = output_dir / f"{libname}.kicad_sym"
    return KicadLibrary(str(library_path))

def build_query(where_clause: str) -> str:
    return f"""
WITH replacements(original, changed) AS (
    VALUES
        (' @ ', '@'),
        ('mA 1 ', 'mA '),
        ('Ohm', 'Ω'),
        ('ohm', 'Ω'),
        ('Ωs', 'Ω'),
        (' Ω', 'Ω'),
        (' kΩ', 'kΩ'),
        (' MΩ', 'MΩ')
)
SELECT
    CAST('C' || lcsc AS varchar) AS lcsc_part,
    manufacturer,
    mfr AS mpn,
    (
        SELECT COALESCE(MAX(result), Description)
        FROM (
            SELECT REPLACE(desc_col, original, changed) AS result
            FROM replacements
            CROSS JOIN (SELECT Description AS desc_col) AS t
        ) AS description_replacements
    ) AS description,
    datasheet,
    stock,
    price
FROM jlc_components
WHERE {where_clause}
"""

def get_price(pricing_string, quantity):
    tiers = pricing_string.split(",")

    for tier in tiers:
        range_part, pricing_part = tier.split(":")
        pricing = float(pricing_part)

        start, end = range_part.split("-")
        start = int(start)
        end = float("inf") if end == "" else int(end)

        if start <= quantity <= end:
            return pricing

    raise ValueError(f"No pricing tier found for quantity {quantity}")

def parse_matches(description: str, PATTERNS: dict):
    matches = {}
    for key, pattern in PATTERNS.items():
        match = pattern.search(description)
        matches[key] = match.group() if match else None
    return matches


def append_parts(conn, name_template, footprint, libname,
                 where_clause, symbol_pins, output_dir, reference=None, ref_text_posx=None, ref_text_posy=None,
                 val_text_posx=None, val_text_posy=None, ref_text_rotation=None,
                 val_text_rotation=None, value_template=None,
                 symbol_rectangles=None, symbol_polylines=None,
                 symbol_arcs=None, keywords="", fp_filters="",
                 ref_text_h_justify=None,ref_text_v_justify=None,
                 val_text_h_justify=None,val_text_v_justify=None,
                 hide_pin_numbers=None,hide_pin_names=None,
                 pin_names_offset=None, extends_symbol_name=None):
    cursor = conn.cursor()
    cursor.execute(build_query(where_clause))

    for lcsc_part, mfg_name, mfg_part, description, datasheet, stock, price in cursor.fetchall():
        try:
            matches = parse_matches(description, PATTERNS)
            value = eval(value_template)
            name = eval(name_template)
            if value is None:
                print(f"Skipping {lcsc_part}: no parsed value from {description!r}")
                continue
        except Exception:
            print(f"Can't parse, skipping {lcsc_part} {description!r}")
            continue

        safe_name = re.sub(r'[\\/:*?"<>|]+', '_', name).strip(" .")
        lib = create_library(safe_name,output_dir)

        clean_description = re.sub(r'[^-A-Za-z 0-9%()℃~+-,±@Ω/\\.]', '', description.strip())
        new_symbol = KicadSymbol.new(
            name, libname, footprint, datasheet, keywords, clean_description, fp_filters
        )
        lib.symbols.append(new_symbol)
        new_symbol.add_default_properties()

        if extends_symbol_name is not None:
            new_symbol.extends = extends_symbol_name

        ref = new_symbol.get_property("Reference")
        if reference is not None:
            ref.value = reference
        else:
            ref.value = "U"
        if ref_text_posx is not None:
            ref.posx = ref_text_posx
        if ref_text_posy is not None:
            ref.posy = ref_text_posy
        if ref_text_rotation is not None:
            ref.rotation = ref_text_rotation
        if ref_text_h_justify is not None:
            ref.effects.h_justify = ref_text_h_justify
        if ref_text_v_justify is not None:
            ref.effects.v_justify = ref_text_v_justify

        val = new_symbol.get_property("Value")
        val.value = value
        if val_text_posx is not None:
            val.posx = val_text_posx
        if val_text_posy is not None:
            val.posy = val_text_posy
        if val_text_rotation is not None:
            val.rotation = val_text_rotation
        if val_text_h_justify is not None:
            val.effects.h_justify = val_text_h_justify
        if val_text_v_justify is not None:
            val.effects.v_justify = val_text_v_justify

        new_symbol.properties.append(Property("LCSC", lcsc_part, is_hidden=True))
        new_symbol.properties.append(Property("MFG", mfg_name, is_hidden=True))
        new_symbol.properties.append(Property("MFGPN", mfg_part, is_hidden=True))
        new_symbol.properties.append(Property("Stock", str(stock), is_hidden=True))
        new_symbol.properties.append(Property("Price@10", str(get_price(price, 10)), is_hidden=True))
        new_symbol.properties.append(Property("Price@100", str(get_price(price, 100)), is_hidden=True))
        new_symbol.properties.append(Property("Price@1000", str(get_price(price, 1000)), is_hidden=True))

        if hide_pin_numbers is not None:
            new_symbol.hide_pin_numbers = hide_pin_numbers
        if pin_names_offset is not None:
            new_symbol.pin_names_offset = pin_names_offset
        if hide_pin_names is not None:
            new_symbol.hide_pin_names = hide_pin_names

        for pin in symbol_pins or []:
            new_symbol.pins.append(pin)
        for rectangle in symbol_rectangles or []:
            new_symbol.rectangles.append(rectangle)
        for polyline in symbol_polylines or []:
            new_symbol.polylines.append(polyline)
        for arc in symbol_arcs or []:
            new_symbol.arcs.append(arc)

        lib.write()
