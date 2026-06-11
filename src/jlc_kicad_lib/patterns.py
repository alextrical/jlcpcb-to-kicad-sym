import re

CAPACITANCE_RE = re.compile(r'\d+(?:\.\d+)?\s*(?:pF|nF|uF|F)', re.I)
DIELECTRIC_RE = re.compile(r'(?:X[578][RST]|X6S|X7S|X7T|X8R|C0G|NP0|C0H|U2J|T2H|S2H|R2H|P2H|Y5V|Y5U)', re.I)
TOLERANCE_RE = re.compile(r'(?:[±+-]\d+%|-\d+%~[+-]?\d+%)', re.I)
CURRENT_RE = re.compile(r'\d+(?:\.\d+)?\s*(?:mA|µA|uA|A|kA)', re.I)
RESISTANCE_RE = re.compile(r'\d+(?:\.\d+)?\s*(?:Ω|ohm|mΩ|kΩ|MΩ|GΩ|kohm|Mohm|Z|Z\d+)', re.I)
IMPEDANCE_RE = re.compile(r'\d+(?:\.\d+)?\s*(?:Ω|ohm|kΩ|MΩ|Z|Z\d+)', re.I)
FREQUENCY_RE = re.compile(r'\d+(?:\.\d+)?\s*(?:Hz|kHz|MHz|GHz|THz)', re.I)
VOLTAGE_RE = re.compile(r'\d+(?:\.\d+)?\s*(?:~|-|to)\s*\d+(?:\.\d+)?\s*V|\d+(?:\.\d+)?\s*k?V', re.I)
WAVELENGTH_RE = re.compile(r'\d+(?:\.\d+)?\s*(?:~|-|to)\s*\d+(?:\.\d+)?\s*nm|\d+(?:\.\d+)?\s*nm', re.I)
BRIGHTNESS_RE = re.compile(r'\d+(?:\.\d+)?\s*(?:mcd|cd)', re.I)
POWER_RE = re.compile(r'\d+(?:\.\d+)?\s*(?:mW|W|kW)', re.I)
COLOUR_RE = re.compile(r'\b(?:red|green|blue|yellow|amber|orange|white|warm\s+white|natural\s+white|neutral\s+white|cool\s+white|rgb|pink|purple|violet|uv|infrared|ir)\b', re.I)

PATTERNS = {
    'voltage': VOLTAGE_RE,
    'tolerance': TOLERANCE_RE,
    'capacitance': CAPACITANCE_RE,
    'dielectric': DIELECTRIC_RE,
    'current': CURRENT_RE,
    'resistance': RESISTANCE_RE,
    'impedance': IMPEDANCE_RE,
    'frequency': FREQUENCY_RE,
    'wavelength': WAVELENGTH_RE,
    'brightness': BRIGHTNESS_RE,
    'power': POWER_RE,
    'colour': COLOUR_RE,
}
