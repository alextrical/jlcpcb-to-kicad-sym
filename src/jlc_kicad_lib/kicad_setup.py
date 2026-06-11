import sys

sys.path.append("kicad-library-utils/common")

from kicad_sym import Pin, Polyline, Point, Arc, Rectangle


def diode_pins():
    return [
        Pin(name="K", number="1", etype="passive", posx=-3.81, posy=0, rotation=0, length=2.54),
        Pin(name="A", number="2", etype="passive", posx=3.81, posy=0, rotation=180, length=2.54),
    ]


def diode_polylines():
    return [
        Polyline(points=[Point(x=-1.27, y=0), Point(x=1.27, y=0)], stroke_width=0),
        Polyline(points=[Point(x=-1.27, y=-1.27), Point(x=-1.27, y=1.27)], stroke_width=0),
        Polyline(points=[Point(x=1.27, y=-1.27), Point(x=1.27, y=1.27), Point(x=-1.27, y=0), Point(x=1.27, y=-1.27)], stroke_width=0),
    ]

def resistor_pins():
    return [
        Pin(name="", number="1", etype="passive", posx=0, posy=3.81, rotation=270, length=1.27),
        Pin(name="", number="2", etype="passive", posx=0, posy=-3.81, rotation=90, length=1.27),
    ]

def resistor_rectangles():
    return [
        Rectangle(startx=-1.016, starty=-2.54, endx=1.016, endy=2.54, fill_type="none", stroke_width=0.254),
    ]

def capacitor_pins():
    return [
        Pin(name="~", number="1", etype="passive", posx=0, posy=3.81, rotation=270, length=2.794),
        Pin(name="~", number="2", etype="passive", posx=0, posy=-3.81, rotation=90, length=2.794),
    ]

def capacitor_polylines():
    return [
        Polyline(points=[Point(x=-2.032, y=-0.762), Point(x=2.032, y=-0.762) ], stroke_width=0.508),
        Polyline(points=[Point(x=-2.032, y=+0.762), Point(x=2.032, y=+0.762) ], stroke_width=0.508),
    ]

def ferrite_bead_pins():
    return [
        Pin(name="~", number="1", etype="passive", posx=0, posy=3.81, rotation=270, length=2.54),
        Pin(name="~", number="2", etype="passive", posx=0, posy=-3.81, rotation=90, length=2.54),
    ]

def ferrite_bead_polylines():
    return [
        Polyline(points=[Point(x=0, y=1.27), Point(x=0, y=1.2954) ], stroke_width=0),
        Polyline(points=[Point(x=-2.7686, y=0.4064), Point(x=-1.7018, y=2.2606), Point(x=2.7686, y=-0.3048), Point(x=1.6764, y=-2.1590), Point(x=-2.7686, y=0.4064) ], stroke_width=0),
    ]

def led_polylines():
    return [
        Polyline(points=[Point(x=-3.048, y=-0.762), Point(x=-4.572, y=-2.286), Point(x=-3.81, y=-2.286), Point(x=-4.572, y=-2.286), Point(x=-4.572, y=-1.524) ], stroke_width=0),
        Polyline(points=[Point(x=-1.778, y=-0.762), Point(x=-3.302, y=-2.286), Point(x=-2.54, y=-2.286), Point(x=-3.302, y=-2.286), Point(x=-3.302, y=-1.524) ], stroke_width=0),
        Polyline(points=[Point(x=-1.27, y=0), Point(x=1.27, y=0) ], stroke_width=0),
        Polyline(points=[Point(x=-1.27, y=-1.27), Point(x=-1.27, y=1.27) ], stroke_width=0),
        Polyline(points=[Point(x=1.27, y=-1.27), Point(x=1.27, y=1.27), Point(x=-1.27, y=0), Point(x=1.27, y=-1.27) ], stroke_width=0),
    ]

def inductor_arcs():
    return [
        Arc(startx=0.0, starty=0.0, endx=0.0, endy=0.508, midx=0.254, midy=0.254, stroke_width=0.2032),
    ]

def inductor_pins():
    return [
        Pin(name="~", number="1", etype="passive", posx=0, posy=3.81, rotation=270, length=2.54),
        Pin(name="~", number="2", etype="passive", posx=0, posy=-3.81, rotation=90, length=2.54),
    ]

def diode_schottky_polylines():
    return [
    Polyline(points=[Point(x=-1.27, y=0), Point(x=1.27, y=0) ], stroke_width=0),
    Polyline(points=[Point(x=-1.905, y=0.635), Point(x=-1.905, y=1.27), Point(x=-1.27, y=1.27), Point(x=-1.27, y=-1.27), Point(x=-0.635, y=-1.27), Point(x=-0.635, y=-0.635) ], stroke_width=0),
    Polyline(points=[Point(x=1.27, y=-1.27), Point(x=1.27, y=1.27), Point(x=-1.27, y=0), Point(x=1.27, y=-1.27) ], stroke_width=0),
    ]

def diode_zener_polylines():
    return [
    Polyline(points=[Point(x=-1.27, y=0), Point(x=1.27, y=0) ], stroke_width=0),
    Polyline(points=[Point(x=-1.27, y=-1.27), Point(x=-1.27, y=1.27), Point(x=-0.762, y=1.27) ], stroke_width=0),
    Polyline(points=[Point(x=1.27, y=-1.27), Point(x=1.27, y=1.27), Point(x=-1.27, y=0), Point(x=1.27, y=-1.27) ], stroke_width=0),
    ]

# def ():
#     return [
#     ]