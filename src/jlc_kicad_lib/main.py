#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import Callable, Optional

from generator import append_parts, create_connection, create_library
from symbols import *
from footprint_packages import *


BASE_FILTER = '(library_type = "base" OR preferred = 1)'


@dataclass(frozen=True)
class LibrarySpec:
    libname: str
    package_source: Callable
    name_template: str
    value_template: str
    reference: str
    category_filter: str
    symbol_pins: object
    symbol_polylines: Optional[object] = None
    symbol_rectangles: Optional[object] = None
    text_kwargs: dict = field(default_factory=dict)


def build_library(conn, spec: LibrarySpec) -> None:
    # lib = create_library(spec.libname)

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
            reference=spec.reference,
            footprint=footprint_name,
            libname=spec.libname,
            where_clause=where_clause,
            symbol_pins=spec.symbol_pins,
            **spec.text_kwargs,
        )

        if spec.symbol_polylines is not None:
            kwargs["symbol_polylines"] = spec.symbol_polylines
        if spec.symbol_rectangles is not None:
            kwargs["symbol_rectangles"] = spec.symbol_rectangles

        append_parts(**kwargs)


LIBRARIES = [
    # LibrarySpec(
    #     libname="JLCPCB_Basic_Diode-General",
    #     package_source=diode_packages,
    #     name_template="mfg_part",
    #     value_template="mfg_part",
    #     reference="D",
    #     category_filter='category="Diodes" and "Subcategory"="Diodes - General Purpose"',
    #     symbol_pins=diode_pins(),
    #     symbol_polylines=diode_polylines(),
    #     text_kwargs={
    #         "ref_text_posy": 2.54, 
    #         "val_text_posy": -2.54,
    #         "keywords": "diode",
    #         "fp_filters": "TO-???* *_Diode_* *SingleDiode* D_*",
    #         "hide_pin_numbers": True,
    #         "hide_pin_names": True,
    #     },
    # ),
    # LibrarySpec(
    #     libname="JLCPCB_Basic_Resistor",
    #     package_source=resistor_packages,
    #     name_template="'_'.join(filter(None, [matches['resistance'], '{package_name}', matches['tolerance']]))",
    #     value_template="re.sub(r'[^a-zA-Z0-9.]', '', matches['resistance'])",
    #     reference="R",
    #     category_filter='"Category" = "Resistors" and "Subcategory" = "Chip Resistor - Surface Mount"',
    #     symbol_pins=resistor_pins(),
    #     symbol_rectangles=resistor_rectangles(),
    #     text_kwargs={
    #         "ref_text_posx": 2.032,
    #         "ref_text_rotation": 90,
    #         "val_text_rotation": 90,
    #         "keywords": "R res resistor",
    #         "fp_filters": "R_*",
    #         "hide_pin_numbers": True,
    #         "hide_pin_names": True,
    #     },
    # ),
    # LibrarySpec(
    #     libname="JLCPCB_Basic_Capacitor",
    #     package_source=capacitor_packages,
    #     name_template="'_'.join(filter(None, [matches['capacitance'], '{package_name}', matches['voltage'], matches['dielectric'], matches['tolerance']]))",
    #     value_template="matches['capacitance']",
    #     reference="C",
    #     category_filter='"Category" = "Capacitors" and "Subcategory" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT"',
    #     symbol_pins=capacitor_pins(),
    #     symbol_rectangles=capacitor_polylines(),
    #     text_kwargs={
    #         "ref_text_posx": 0.635,
    #         "val_text_posx": 0.635,
    #         "ref_text_posy": 2.54,
    #         "val_text_posy": -2.54,
    #         "val_text_h_justify": "left",
    #         "ref_text_h_justify": "left",
    #         "keywords": "cap capacitor",
    #         "fp_filters": "C_",
    #         "hide_pin_numbers": True,
    #         "hide_pin_names": True,
    #     },
    # ),
    # LibrarySpec(
    #     libname="JLCPCB_Basic_FerriteBead",
    #     package_source=ferritebead_packages,
    #     name_template="'_'.join(filter(None, [matches['impedance'] + '@' + matches['frequency'], '{package_name}', matches['current'], matches['tolerance']]))",
    #     value_template="matches['impedance'] + '@' + matches['frequency']",
    #     reference="FB",
    #     category_filter='"Subcategory" LIKE "Ferrite Beads"',
    #     symbol_pins=ferrite_bead_pins(),
    #     symbol_polylines=ferrite_bead_polylines(),
    #     text_kwargs={
    #         "ref_text_posx": -3.81,
    #         "ref_text_posy": 0.635,
    #         "ref_text_rotation": 90,
    #         "val_text_posx": 3.81,
    #         "val_text_rotation": 90,
    #         "keywords": "L ferrite bead inductor filter",
    #         "fp_filters": "Inductor_* L_* *Ferrite*",
    #         "hide_pin_numbers": True,
    #         "hide_pin_names": True,
    #     },
    # ),
    # LibrarySpec(
    #     libname="JLCPCB_Basic_LED",
    #     package_source=resistor_packages,
    #     name_template="'_'.join(filter(None, [matches['colour'], '{package_name}', matches['current'], matches['brightness']]))",
    #     value_template="matches['colour']",
    #     reference="D",
    #     category_filter='category="Optoelectronics" and "Subcategory"="LED Indication - Discrete"',
    #     symbol_pins=diode_pins(),
    #     symbol_polylines=led_polylines(),
    #     text_kwargs={
    #         "ref_text_posy": 2.54, 
    #         "val_text_posy": -2.54,
    #         "keywords": "LED diode",
    #         "fp_filters": "LED* LED_SMD:* LED_THT:*",
    #         "hide_pin_numbers": True,
    #         "hide_pin_names": True,
    #     },
    # ),
    # LibrarySpec(
    #     libname="JLCPCB_Basic_Diode-Zener",
    #     package_source=diode_packages,
    #     name_template="mfg_part",
    #     value_template="mfg_part",
    #     reference="D",
    #     category_filter='category="Diodes" and "Subcategory"="Zener Diodes"',
    #     symbol_pins=diode_pins(),
    #     symbol_polylines=diode_zener_polylines(),
    #     text_kwargs={
    #         "ref_text_posy": 2.54, 
    #         "val_text_posy": -2.54,
    #         "keywords": "diode Zener",
    #         "fp_filters": "TO-???* *_Diode_* *SingleDiode* D_*",
    #         "hide_pin_numbers": True,
    #         "hide_pin_names": True,
    #     },
    # ),
    LibrarySpec(
        libname="JLCPCB_Basic_Diode-Schottky",
        # extends="Device.kicad_symdir/D_Schottky.kicad_sym",
        package_source=diode_packages,
        name_template="mfg_part",
        value_template="mfg_part",
        reference="D",
        category_filter='category="Diodes" and "Subcategory"="Schottky Diodes"',
        symbol_pins=diode_pins(),
        symbol_polylines=diode_schottky_polylines(),
        text_kwargs={
            "ref_text_posy": 2.54, 
            "val_text_posy": -2.54,
            "keywords": "diode Schottky",
            "fp_filters": "TO-???* *_Diode_* *SingleDiode* D_*",
            "hide_pin_numbers": True,
            "hide_pin_names": True,
        },
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
