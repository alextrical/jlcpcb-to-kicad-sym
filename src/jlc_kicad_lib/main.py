#!/usr/bin/env python3
from generator import create_connection, create_library, append_parts
from kicad_setup import diode_pins, diode_polylines, resistor_pins, resistor_rectangles, capacitor_pins, capacitor_polylines, ferrite_bead_pins, ferrite_bead_polylines, led_polylines, inductor_arcs, inductor_pins, diode_schottky_polylines, diode_zener_polylines
from symbols.diodes import general_diode_packages
from symbols.passives import general_resistor_packages


def build_basic_diodes(conn):
    libname = "JLCPCB_Basic_Diode-General"
    lib = create_library(libname)
    for package_name, footprint_name, package_match in general_diode_packages():
        append_parts(
            conn=conn,
            lib=lib,
            name_template="mfg_part",
            value_template="mfg_part",
            reference="D",
            footprint=footprint_name,
            libname=libname,
            where_clause=(
                '(library_type = "base" OR preferred = 1) '
                'and category="Diodes" '
                'and "Subcategory"="Diodes - General Purpose" '
                'and Package ' + package_match
            ),
            symbol_pins=diode_pins(),
            symbol_polylines=diode_polylines(),
            # ref_text_posx=0,
            ref_text_posy=2.54,
            # val_text_posx=0,
            val_text_posy=-2.54,
            # ref_text_rotation=0,
            # val_text_rotation=0,
            # keywords="",
            # fp_filters="",
        )

def build_basic_resistors(conn):
    libname = "JLCPCB_Basic_Resistor"
    lib = create_library(libname)
    for package_name, footprint_name, package_match in general_resistor_packages():
        append_parts(
            conn=conn,
            lib=lib,
            name_template="'_'.join(filter(None, [matches['resistance'], '" + package_name + "', matches['tolerance']]))",
            value_template="matches['resistance']",
            reference="R",
            footprint=footprint_name,
            libname=libname,
            where_clause=(
                '(library_type = "base" OR preferred = 1) '
                'and "Category" = "Resistors" '
                'and "Subcategory" = "Chip Resistor - Surface Mount" '
                'and Package ' + package_match
            ),
            symbol_pins=resistor_pins(),
            symbol_rectangles=resistor_rectangles(),
            ref_text_posx=0.762,
            val_text_posx=0.762,
            ref_text_posy=2.54,
            val_text_posy=-2.54,
        )

def main():
    conn = create_connection('build/cache.sqlite3')
    try:
        # build_basic_diodes(conn)
        build_basic_resistors(conn)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
