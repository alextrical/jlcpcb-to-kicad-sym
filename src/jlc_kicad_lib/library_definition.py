from dataclasses import dataclass
from typing import Callable, Optional

from footprint_lookup import *

@dataclass(frozen=True)
class LibrarySpec:
    libname: str
    package_source: Callable
    name_template: str
    value_template: str
    category_filter: str
    extends_symbol: Optional[str] = None
    extends_symbol_lookup: Optional[dict[str, str]] = None
    reference: Optional[str] = None

libraries = [
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
        name_template = '"_".join(filter(None,[data.get("Resistance"),package_name,data.get("Tolerance", "")]))',
        value_template="re.sub(r'[^a-zA-Z0-9.]', '', data['Resistance'])",
        category_filter='"Category" = "Resistors" and "Subcategory" = "Chip Resistor - Surface Mount"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_Capacitor_MLCC",
        extends_symbol="Device.kicad_symdir/C.kicad_sym",
        package_source=capacitor_packages,
        name_template = '"_".join(filter(None,[data.get("Capacitance"),package_name,data.get("Voltage Rating", ""),data.get("Temperature Coefficient", ""),data.get("Tolerance", "")]))',
        value_template="data['Capacitance']",
        category_filter='"Category" = "Capacitors" and "Subcategory" = "Multilayer Ceramic Capacitors MLCC - SMD/SMT"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_FerriteBead",
        extends_symbol="Device.kicad_symdir/FerriteBead.kicad_sym",
        package_source=ferritebead_packages,
        name_template = '"_".join(filter(None,[data.get("Impedance @ Frequency"),package_name,data.get("Current Rating", ""),data.get("Tolerance", "")]))',
        value_template="data['Impedance @ Frequency']",
        category_filter='"Subcategory" LIKE "Ferrite Beads"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_LED",
        extends_symbol="Device.kicad_symdir/LED.kicad_sym",
        package_source=led_packages,
        name_template = '"_".join(filter(None,[data.get("Illumination Color", "").replace(" ", "_"),package_name,data.get("Forward Current", ""),data.get("Luminous Intensity", "")]))',
        value_template="data['Illumination Color']",
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
    LibrarySpec(
        libname="JLCPCB_Basic_Mosfet_NPN",
        extends_symbol_lookup={
            "2N7002*": "Transistor_FET.kicad_symdir/Q_NMOS_GSD.kicad_sym",
            "AO3400*": "Transistor_FET.kicad_symdir/Q_NMOS_GSD.kicad_sym",
            "HL2303": "Transistor_FET.kicad_symdir/Q_NMOS_GSD.kicad_sym",
            "BSS1*": "Transistor_FET.kicad_symdir/Q_NMOS_GSD.kicad_sym",
            "HL2*": "Transistor_FET.kicad_symdir/Q_NMOS_GSD.kicad_sym",
            "HL3*": "Transistor_FET.kicad_symdir/Q_NMOS_GSD.kicad_sym",
            "FDV301N": "Transistor_FET.kicad_symdir/Q_NMOS_GSD.kicad_sym",
            "2SK3018": "Transistor_FET.kicad_symdir/Q_NMOS_GSD.kicad_sym",
            "MDD2302": "Transistor_FET.kicad_symdir/Q_NMOS_GSD.kicad_sym",
        },
        package_source=transistor_packages,
        name_template="mfg_part",
        value_template="mfg_part",
        category_filter='LOWER(category)="transistors/thyristors" and LOWER(Subcategory)="mosfets" and LOWER(json_extract(attributes, "$.Number")) = "1 n-channel"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_Mosfet_PNP",
        extends_symbol_lookup={
            "LBSS84*": "Transistor_FET.kicad_symdir/Q_PMOS_GSD.kicad_sym",
            "AO3401*": "Transistor_FET.kicad_symdir/Q_PMOS_GSD.kicad_sym",
            "MDD*": "Transistor_FET.kicad_symdir/Q_PMOS_GSD.kicad_sym",
            "SI2301*": "Transistor_FET.kicad_symdir/Q_PMOS_GSD.kicad_sym",
            "BSS84": "Transistor_FET.kicad_symdir/Q_PMOS_GSD.kicad_sym",
            "HL2*": "Transistor_FET.kicad_symdir/Q_PMOS_GSD.kicad_sym",
            "HL3*": "Transistor_FET.kicad_symdir/Q_PMOS_GSD.kicad_sym",
            "HL6*": "Transistor_FET.kicad_symdir/Q_PMOS_GSD.kicad_sym",
        },
        package_source=transistor_packages,
        name_template="mfg_part",
        value_template="mfg_part",
        category_filter='LOWER(category)="transistors/thyristors" and LOWER(Subcategory)="mosfets" and LOWER(json_extract(attributes, "$.Number")) = "1 p-channel"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_BJT_NPN",
        extends_symbol_lookup={
            "2SC4672": "Transistor_BJT.kicad_symdir/Q_NPN_BCE.kicad_sym",
            "2SC2873": "Transistor_BJT.kicad_symdir/Q_NPN_BCE.kicad_sym",
            "2SC2884": "Transistor_BJT.kicad_symdir/Q_NPN_BCE.kicad_sym",
            "D882*": "Transistor_BJT.kicad_symdir/Q_NPN_BCE.kicad_sym",
            "BCX56-1*": "Transistor_BJT.kicad_symdir/Q_NPN_BCE.kicad_sym",

            "MMBT2*": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "MMBT3*": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "MMBT4*": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "MMBT5*": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "S9013*": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "BC8*": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "S8050*": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "SS8050*": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "MMBTA*": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "2SC1623": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "2SC1815": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "2SC3356": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "S9014": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "FMMT493": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
            "MMST3904": "Transistor_BJT.kicad_symdir/Q_NPN_BEC.kicad_sym",
        },
        package_source=transistor_packages,
        name_template="mfg_part",
        value_template="mfg_part",
        category_filter='LOWER(category)="transistors/thyristors" and LOWER(Subcategory)="bipolar (bjt)" and LOWER(json_extract(attributes, "$.type")) = "npn"',
    ),
    LibrarySpec(
        libname="JLCPCB_Basic_BJT_PNP",
        extends_symbol_lookup={
            "B772*": "Transistor_BJT.kicad_symdir/Q_PNP_BCE.kicad_sym",
            "2SA1213*": "Transistor_BJT.kicad_symdir/Q_PNP_BCE.kicad_sym",

            "S9015*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "MMBT5401*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "SS8550*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "S8550*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "S9012*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "2SA812*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "MMBT2907A*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "MMBT3906*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "BC856B*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "BC857C*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "MMBT4403*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "BC807-40*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "MMBTA92*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            "MMBTA56*": "Transistor_BJT.kicad_symdir/Q_PNP_BEC.kicad_sym",
            
        },
        package_source=transistor_packages,
        name_template="mfg_part",
        value_template="mfg_part",
        category_filter='LOWER(category)="transistors/thyristors" and LOWER(Subcategory)="bipolar (bjt)" and LOWER(json_extract(attributes, "$.type")) = "pnp"',
    ),
]