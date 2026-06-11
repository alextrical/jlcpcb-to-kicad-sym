import re
import sqlite3
import sys

sys.path.append("scripts/kicad-library-utils/common")
import kicad_sym

from kicad_sym import KicadLibrary, KicadSymbol, Property
from patterns import PATTERNS


def create_connection(db_path: str):
    return sqlite3.connect(db_path)


def create_library(libname: str):
    return KicadLibrary(libname + ".kicad_sym")


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
    datasheet
FROM jlc_components
WHERE {where_clause}
"""


def parse_matches(description: str, PATTERNS: dict):
    matches = {}
    for key, pattern in PATTERNS.items():
        match = pattern.search(description)
        matches[key] = match.group() if match else None
    return matches


def append_parts(conn, lib, name_template, reference, footprint, libname,
                 where_clause, symbol_pins, ref_text_posx=0, ref_text_posy=0,
                 val_text_posx=0, val_text_posy=0, ref_text_rotation=0,
                 val_text_rotation=0, value_template=None,
                 symbol_rectangles=None, symbol_polylines=None,
                 symbol_arcs=None, keywords="", fp_filters=""):
    cursor = conn.cursor()
    cursor.execute(build_query(where_clause))

    for lcsc_part, mfg_name, mfg_part, description, datasheet in cursor.fetchall():
        try:
            matches = parse_matches(description, PATTERNS)
            scope = {**matches, 'mfg_part': mfg_part, 'description': description}
            value = eval(value_template, {}, scope)
            name = eval(name_template, {}, scope)
            if value is None:
                print(f"Skipping {lcsc_part}: no parsed value from {description!r}")
                continue
        except Exception:
            print(f"Can't parse, skipping {lcsc_part} {description!r}")
            continue

        clean_description = re.sub(r'[^-A-Za-z 0-9%()℃~+-,±@Ω/\\.]', '', description.strip())
        new_symbol = KicadSymbol.new(
            name, libname, reference, footprint, datasheet, keywords, clean_description, fp_filters
        )
        lib.symbols.append(new_symbol)
        new_symbol.add_default_properties()

        ref = new_symbol.get_property("Reference")
        ref.posx = ref_text_posx
        ref.posy = ref_text_posy
        ref.rotation = ref_text_rotation

        val = new_symbol.get_property("Value")
        val.value = value
        val.posx = val_text_posx
        val.posy = val_text_posy
        val.rotation = val_text_rotation

        new_symbol.properties.append(Property("LCSC", lcsc_part, is_hidden=True))
        new_symbol.properties.append(Property("MFG", mfg_name, is_hidden=True))
        new_symbol.properties.append(Property("MFGPN", mfg_part, is_hidden=True))

        for pin in symbol_pins:
            new_symbol.pins.append(pin)
        for rectangle in symbol_rectangles or []:
            new_symbol.rectangles.append(rectangle)
        for polyline in symbol_polylines or []:
            new_symbol.polylines.append(polyline)
        for arc in symbol_arcs or []:
            new_symbol.arcs.append(arc)

    lib.write()
