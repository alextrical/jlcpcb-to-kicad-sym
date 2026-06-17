import sexpdata

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


def extract_justify(part):
    """Extract justify tokens from a property's effects block"""
    for sub in part[3:]:
        if isinstance(sub, list) and len(sub) >= 1:
            sub_first = sub[0]
            if isinstance(sub_first, sexpdata.Symbol) and sub_first.value() == "effects":
                for effect_item in sub[1:]:
                    if isinstance(effect_item, list) and len(effect_item) >= 1:
                        effect_first = effect_item[0]
                        if isinstance(effect_first, sexpdata.Symbol) and effect_first.value() == "justify":
                            return [get_value(x) for x in effect_item[1:]]
    return []


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


# Usage
result = extract_symbol_properties(
    "../kicad-symbols/Device.kicad_symdir/C.kicad_sym"
)

symbol_name = result.get("symbol_name")
props = result.get("properties", {})

reference = props.get("Reference", {})
value = props.get("Value", {})
ki_fp_filters = props.get("ki_fp_filters", {})
ki_keywords = props.get("ki_keywords", {})

print(f"symbol_name = {symbol_name}")
print(f"Reference = {reference.get('value')}")
print(f"Reference_x = {reference.get('x')}")
print(f"Reference_y = {reference.get('y')}")
print(f"Reference_angle = {reference.get('angle')}")
print(f"Reference_justify = {reference.get('justify')}")
print(f"Value = {value.get('value')}")
print(f"Value_x = {value.get('x')}")
print(f"Value_y = {value.get('y')}")
print(f"Value_angle = {value.get('angle')}")
print(f"Value_justify = {value.get('justify')}")
print(f"ki_fp_filters = {ki_fp_filters.get('value')}")
print(f"ki_keywords = {ki_keywords.get('value')}")
