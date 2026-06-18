import re
import sexpdata
import sys
import shutil
import json

from pathlib import Path
from fnmatch import fnmatchcase

sys.path.append("src/kicad-library-utils/common")
import kicad_sym
from kicad_sym import KicadLibrary, KicadSymbol, Property

from library_definition import libraries, LibrarySpec

def build_library(conn, spec: LibrarySpec, root_dir, output_folder) -> None:
    output_dir = Path(root_dir) / Path(output_folder) / f"{spec.libname}.kicad_symdir"
    output_dir.mkdir(parents=True, exist_ok=True)

    kwargs = dict(
        conn=conn,
        name_template=spec.name_template,
        value_template=spec.value_template,
        libname=spec.libname,
        output_dir=output_dir,
        root_dir=root_dir,
        package_source=spec.package_source,
        category_filter=spec.category_filter,
    )

    if spec.extends_symbol_lookup is not None:
        kwargs["extends_symbol_lookup"] = spec.extends_symbol_lookup

    if spec.extends_symbol is not None:
        kwargs["extends_symbol"] = spec.extends_symbol

    append_parts(**kwargs)

def create_library(libname: str, output_dir: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    library_path = output_dir / f"{libname}.kicad_sym"
    return KicadLibrary(str(library_path))

def append_parts(conn, name_template, libname, output_dir, root_dir, category_filter, value_template, package_source,
                 extends_symbol=None, extends_symbol_lookup=None, footprint=None,
                 reference=None, ref_text_posx=None, ref_text_posy=None,
                 val_text_posx=None, val_text_posy=None, ref_text_rotation=None,
                 val_text_rotation=None, 
                 ref_text_h_justify=None,ref_text_v_justify=None,
                 val_text_h_justify=None,val_text_v_justify=None,
                 hide_pin_numbers=None,hide_pin_names=None,
                 pin_names_offset=None, keywords="", fp_filters="",
                # value_template=None, symbol_pins=None, symbol_rectangles=None, symbol_polylines=None,
                # symbol_arcs=None,  extends_symbol_name=None, extends_symbol_lookup=None,package_source=None
                ):

    for package_name, footprint_name, package_match in package_source():
        where_clause = (
            f"(library_type = 'base' OR preferred = 1) "
            f"and {category_filter} "
            f"and Package {package_match}"
        )

        cursor = conn.cursor()
        cursor.execute(build_query(where_clause))

        for lcsc_part, mfg_name, mfg_part, description, attributes, datasheet, stock, price in cursor.fetchall():
            data = json.loads(attributes)
            try:
                value = eval(value_template)
                if value is None:
                    print(f"Skipping {lcsc_part}: no parsed value from {eval(value_template)!r}")
                    continue
            except Exception:
                print(f"Can't parse value, skipping {lcsc_part} {eval(value_template)!r}")
                continue

            try:
                name = eval(name_template)
                if value is None:
                    print(f"Skipping {lcsc_part}: no parsed name_template value from {eval(name_template)!r}")
                    continue
            except Exception:
                print(f"Can't parse name_template, skipping {lcsc_part} {eval(name_template)!r}")
                continue

            extends_symbol_name = None
            source_relpath = None
            if extends_symbol_lookup is not None:
                # source_relpath = extends_symbol_lookup.get(mfg_part)
                for pattern, symbol in extends_symbol_lookup.items():
                    if fnmatchcase(mfg_part, pattern):
                        source_relpath = symbol
                if source_relpath is  None:
                    print(f"Skipping {lcsc_part}: no symbol match for {mfg_part}")
                    continue
            elif extends_symbol is not None:
                source_relpath = extends_symbol
            else:
                print(f"Skipping {lcsc_part}: no symbol")
                continue

            if source_relpath is not None:
                source_file = root_dir / Path("src/kicad-symbols") / source_relpath
                shutil.copy(source_file, output_dir)

                result = extract_symbol_properties(source_file)
                extends_symbol_name = result.get("symbol_name")

                properties = result.get("properties", {})

                reference_prop = properties.get("Reference", {})
                reference = reference_prop["value"]
                ref_text_posx = reference_prop["x"]
                ref_text_posy = reference_prop["y"]
                ref_text_rotation = reference_prop["angle"]
                ref_text_h_justify = reference_prop["justify"]

                value_prop = properties.get("Value", {})
                val_text_posx = value_prop["x"]
                val_text_posy = value_prop["y"]
                val_text_rotation = value_prop["angle"]
                val_text_h_justify = value_prop["justify"]

                fp_filters = properties.get("ki_fp_filters", {}).get("value")
                keywords = properties.get("ki_keywords", {}).get("value")
            
            # print(keywords)

            clean_name = re.sub(r'[\\/:*?"<>|]+', '_', name).strip(" .")
            lib = create_library(clean_name,output_dir)

            clean_description = re.sub(r'[^-A-Za-z 0-9%()℃~+-,±@Ω/\\.]', '', description.strip())
            new_symbol = KicadSymbol.new(
                name=name,
                libname=libname,
                datasheet=datasheet,
                description=clean_description,
                footprint=footprint_name,
            )
            lib.symbols.append(new_symbol)

            ref = new_symbol.get_property("Reference")
            apply_updates(ref, {
                "value": reference,
                "posx": ref_text_posx,
                "posy": ref_text_posy,
                "rotation": ref_text_rotation,
                "effects.h_justify": ref_text_h_justify,
                "effects.v_justify": ref_text_v_justify,
            })

            val = new_symbol.get_property("Value")
            apply_updates(val, {
                "value": value,
                "posx": val_text_posx,
                "posy": val_text_posy,
                "rotation": val_text_rotation,
                "effects.h_justify": val_text_h_justify,
                "effects.v_justify": val_text_v_justify,
            })

            apply_updates(new_symbol, {
                "extends": extends_symbol_name,
                "hide_pin_numbers": hide_pin_numbers,
                "pin_names_offset": pin_names_offset,
                "hide_pin_names": hide_pin_names,
                "keywords": keywords,
                "fp_filters": fp_filters,
            })

            new_symbol.properties.append(Property("LCSC", lcsc_part, is_hidden=True))
            new_symbol.properties.append(Property("MFG", mfg_name, is_hidden=True))
            new_symbol.properties.append(Property("MFGPN", mfg_part, is_hidden=True))
            new_symbol.properties.append(Property("Stock", str(stock), is_hidden=True))
            new_symbol.properties.append(Property("unit_price_10", str(get_price(price, 10)), is_hidden=True))
            new_symbol.properties.append(Property("unit_price_100", str(get_price(price, 100)), is_hidden=True))
            new_symbol.properties.append(Property("unit_price_1000", str(get_price(price, 1000)), is_hidden=True))

            # add values from attributes dynamically
            for key, value in data.items():
                new_symbol.properties.append(Property(key, value, is_hidden=True))

            lib.write()

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
    attributes,
    datasheet,
    stock,
    price
FROM jlc_components
WHERE {where_clause}
"""


#Written by AI
def set_if_not_none(obj, attr_path, value):
    if value is None:
        return

    target = obj
    parts = attr_path.split(".")
    for part in parts[:-1]:
        target = getattr(target, part)
    setattr(target, parts[-1], value)

def apply_updates(obj, updates):
    for attr_path, value in updates.items():
        if value is not None:
            set_if_not_none(obj, attr_path, value)

def get_price(pricing_string, quantity):
    tiers = pricing_string.split(",")

    for tier in tiers:
        range_part, pricing_part = tier.split(":")
        pricing = float(pricing_part)

        start, end = range_part.split("-")
        start = int(start)
        end = float("inf") if end == "" else int(end)

        if start <= quantity <= end:
            return f"${pricing}"

    raise ValueError(f"No pricing tier found for quantity {quantity}")

def get_value_from_symbol(sexp):
    """Extract value from sexpdata types"""
    if isinstance(sexp, sexpdata.Symbol):
        return sexp.value()
    elif isinstance(sexp, sexpdata.String):
        return sexp.value()
    elif isinstance(sexp, str):
        return sexp
    elif isinstance(sexp, int) or isinstance(sexp, float):
        return sexp
    return sexp

def extract_symbol_properties(file_path):
    """Extract symbol name and properties from a KiCad .kicad_sym file"""

    with open(file_path, "r") as f:
        data = sexpdata.load(f)

    result = {
        "symbol_name": None,
        "properties": {},
    }

    # Find top-level symbol
    for item in data:
        if isinstance(item, list) and len(item) > 1:
            first = item[0]
            if isinstance(first, sexpdata.Symbol) and first.value() == "symbol":
                result["symbol_name"] = get_value_from_symbol(item[1])

                for part in item[2:]:
                    if isinstance(part, list) and len(part) >= 3:
                        part_first = part[0]
                        if isinstance(part_first, sexpdata.Symbol) and part_first.value() == "property":
                            prop_name = get_value_from_symbol(part[1])
                            prop_value = get_value_from_symbol(part[2])

                            x, y, angle = None, None, None
                            justify = []

                            for sub in part[3:]:
                                if isinstance(sub, list) and len(sub) >= 1:
                                    sub_first = sub[0]

                                    if isinstance(sub_first, sexpdata.Symbol):
                                        if sub_first.value() == "at" and len(sub) >= 4:
                                            x = get_value_from_symbol(sub[1])
                                            y = get_value_from_symbol(sub[2])
                                            angle = get_value_from_symbol(sub[3])

                                        elif sub_first.value() == "effects":
                                            for effect_item in sub[1:]:
                                                if isinstance(effect_item, list) and len(effect_item) >= 1:
                                                    effect_first = effect_item[0]
                                                    if (
                                                        isinstance(effect_first, sexpdata.Symbol)
                                                        and effect_first.value() == "justify"
                                                    ):
                                                        justify = [get_value_from_symbol(x) for x in effect_item[1:]]

                            result["properties"][prop_name] = {
                                "value": prop_value,
                                "x": x,
                                "y": y,
                                "angle": angle,
                                "justify": justify,
                            }

                break

    return result