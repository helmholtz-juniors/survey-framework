import re


def shorten_center_name(long: str) -> str | None:
    # first, search for an acronym in brackets
    m = re.search(r"\(([A-Z]+)\)", long)
    if m:
        return m.group(1)

    # if that failed, just search for an acronym with at least three letters
    m = re.search(r"([A-Z]{3,})", long)
    if m:
        return m.group(1)

    # handle the strange cases manually
    if "Helmholtz-Zentrum Berlin" in long:
        return "HZB"
    elif "Forschungszentrum Jülich" in long:
        return "FZJ"
    elif "Hereon" in long:
        return "Hereon"
    elif "Helmholtz Zentrum München" in long:
        return "Helmholtz Munich"

    # probably not a center
    return None
