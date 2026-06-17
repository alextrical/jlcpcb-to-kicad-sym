#!/usr/bin/env python3

import sexpdata

from dataclasses import dataclass, field
from typing import Callable, Optional

from generator import append_parts, create_connection, create_library
from symbols import *
from footprint_packages import *
from pathlib import Path
import shutil


BASE_FILTER = '(library_type = "base" OR preferred = 1)'
OUTPUT_DIR = Path("build")


@dataclass(frozen=True)
class LibrarySpec:
    libname: str
    package_source: Callable
    name_template: str
    value_template: str
    category_filter: str
    extends_symbol: Optional[str] = None
    reference: Optional[str] = None
    symbol_pins: Optional[object] = None
    symbol_polylines: Optional[object] = None
    symbol_rectangles: Optional[object] = None
    text_kwargs: dict = field(default_factory=dict)

def get_value(sexp):
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
                result["symbol_name"] = get_value(item[1])

                for part in item[2:]:
                    if isinstance(part, list) and len(part) >= 3:
                        part_first = part[0]
                        if isinstance(part_first, sexpdata.Symbol) and part_first.value() == "property":
                            prop_name = get_value(part[1])
                            prop_value = get_value(part[2])

                            x, y, angle = None, None, None
                            justify = []

                            for sub in part[3:]:
                                if isinstance(sub, list) and len(sub) >= 1:
                                    sub_first = sub[0]

                                    if isinstance(sub_first, sexpdata.Symbol):
                                        if sub_first.value() == "at" and len(sub) >= 4:
                                            x = get_value(sub[1])
                                            y = get_value(sub[2])
                                            angle = get_value(sub[3])

                                        elif sub_first.value() == "effects":
                                            for effect_item in sub[1:]:
                                                if isinstance(effect_item, list) and len(effect_item) >= 1:
                                                    effect_first = effect_item[0]
                                                    if (
                                                        isinstance(effect_first, sexpdata.Symbol)
                                                        and effect_first.value() == "justify"
                                                    ):
                                                        justify = [get_value(x) for x in effect_item[1:]]

                            result["properties"][prop_name] = {
                                "value": prop_value,
                                "x": x,
                                "y": y,
                                "angle": angle,
                                "justify": justify,
                            }

                break

    return result

def build_library(conn, spec: LibrarySpec) -> None:

    output_dir = Path(OUTPUT_DIR) / f"{spec.libname}.kicad_symdir"
    output_dir.mkdir(parents=True, exist_ok=True)

    if spec.extends_symbol is not None:
        source_file = Path("../kicad-symbols") / spec.extends_symbol
        shutil.copy(source_file, output_dir)
        result = extract_symbol_properties(source_file)
        extends_symbol_name = result.get("symbol_name")

        props = result.get("properties", {})
        reference = props.get("Reference", {})
        value = props.get("Value", {})
        ki_fp_filters = props.get("ki_fp_filters", {})
        ki_keywords = props.get("ki_keywords", {})

    for package_name, footprint_name, package_match in spec.package_source():
        where_clause = (
            f"{BASE_FILTER} "
            f"and {spec.category_filter} "
            f"and Package {package_match}"
        )

        kwargs = dict(
            conn=conn,
            # lib=lib,
            name_template=spec.name_template.replace("{package_name}", package_name),
            value_template=spec.value_template,
            footprint=footprint_name,
            libname=spec.libname,
            output_dir=output_dir,
            where_clause=where_clause,
            symbol_pins=spec.symbol_pins,
            **spec.text_kwargs,
        )

        if spec.extends_symbol is not None:
            kwargs["extends_symbol_name"] = extends_symbol_name

        if spec.extends_symbol is not None:
            if spec.text_kwargs.get("ref_text_posx", None) is None:
                kwargs["ref_text_posx"] = reference.get('x')
            if spec.text_kwargs.get("ref_text_posy", None) is None:
                kwargs["ref_text_posy"] = reference.get('y')
            if spec.text_kwargs.get("ref_text_h_justify", None) is None:
                kwargs["ref_text_h_justify"] = reference.get('justify')
            if spec.text_kwargs.get("ref_text_rotation", None) is None:
                kwargs["ref_text_rotation"] = reference.get('angle')

            if spec.text_kwargs.get("val_text_posx", None) is None:
                kwargs["val_text_posx"] = value.get('x')
            if spec.text_kwargs.get("val_text_posy", None) is None:
                kwargs["val_text_posy"] = value.get('y')
            if spec.text_kwargs.get("val_text_h_justify", None) is None:
                kwargs["val_text_h_justify"] = value.get('justify')
            if spec.text_kwargs.get("val_text_rotation", None) is None:
                kwargs["val_text_rotation"] = value.get('angle')
                
        if spec.reference is not None:
            kwargs["reference"] = spec.reference
        else:
            kwargs["reference"] = reference.get('value')

        if spec.text_kwargs.get("fp_filters", None) is None:
            kwargs["fp_filters"] = ki_fp_filters.get('value')

        if spec.text_kwargs.get("keywords", None) is None:
            kwargs["keywords"] = ki_keywords.get('value')

        if spec.symbol_polylines is not None:
            kwargs["symbol_polylines"] = spec.symbol_polylines
        if spec.symbol_rectangles is not None:
            kwargs["symbol_rectangles"] = spec.symbol_rectangles

        append_parts(**kwargs)


LIBRARIES = [
    LibrarySpec(
        libname="JLCPCB_Basic_Diode-General",
        extends_symbol="Device.kicad_symdir/D.kicad_sym",
        package_source=diode_packages,
        name_template="mfg_part",
        value_template="mfg_part",
        category_filter='category="Diodes" and "Subcategory"="Diodes - General Purpose"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_Resistor",
        extends_symbol="Device.kicad_symdir/R.kicad_sym",
        package_source=resistor_packages,
        name_template="'_'.join(filter(None, [matches['resistance'], '{package_name}', matches['tolerance']]))",
        value_template="re.sub(r'[^a-zA-Z0-9.]', '', matches['resistance'])",
        category_filter='"Category" = "Resistors" and "Subcategory" = "Chip Resistor - Surface Mount"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_Capacitor",
        extends_symbol="Device.kicad_symdir/C.kicad_sym",
        package_source=capacitor_packages,
        name_template="'_'.join(filter(None, [matches['capacitance'], '{package_name}', matches['voltage'], matches['dielectric'], matches['tolerance']]))",
        value_template="matches['capacitance']",
        category_filter='"Category" = "Capacitors" and "Subcategory" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_FerriteBead",
        extends_symbol="Device.kicad_symdir/FerriteBead.kicad_sym",
        package_source=ferritebead_packages,
        name_template="'_'.join(filter(None, [matches['impedance'] + '@' + matches['frequency'], '{package_name}', matches['current'], matches['tolerance']]))",
        value_template="matches['impedance'] + '@' + matches['frequency']",
        # reference="FB",
        category_filter='"Subcategory" LIKE "Ferrite Beads"',
        # symbol_pins=ferrite_bead_pins(),
        # symbol_polylines=ferrite_bead_polylines(),
        # text_kwargs={
        #     "ref_text_posx": -3.81,
        #     "ref_text_posy": 0.635,
        #     "ref_text_rotation": 90,
        #     "val_text_posx": 3.81,
        #     "val_text_rotation": 90,
        #     "val_text_h_justify": "left",
        #     "ref_text_h_justify": "left",
        #     "keywords": "L ferrite bead inductor filter",
        #     "fp_filters": "Inductor_* L_* *Ferrite*",
        #     "hide_pin_numbers": True,
        #     "hide_pin_names": True,
        # },
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_LED",
        extends_symbol="Device.kicad_symdir/LED.kicad_sym",
        package_source=diode_packages,
        name_template="'_'.join(filter(None, [matches['colour'], '{package_name}', matches['current'], matches['brightness']]))",
        value_template="matches['colour']",
        category_filter='category="Optoelectronics" and "Subcategory"="LED Indication - Discrete"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_Diode-Zener",
        extends_symbol="Device.kicad_symdir/D_Zener.kicad_sym",
        package_source=diode_packages,
        name_template="mfg_part",
        value_template="mfg_part",
        category_filter='category="Diodes" and "Subcategory"="Zener Diodes"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_Diode-Schottky",
        extends_symbol="Device.kicad_symdir/D_Schottky.kicad_sym",
        package_source=diode_packages,
        name_template="mfg_part",
        value_template="mfg_part",
        category_filter='category="Diodes" and "Subcategory"="Schottky Diodes"',
    ),
]


def main() -> None:
    conn = create_connection("cache/cache.sqlite3")
    try:
        for spec in LIBRARIES:
            build_library(conn, spec)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
