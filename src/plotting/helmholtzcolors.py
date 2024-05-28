#!/usr/bin/env python3
"""
Created on Sun Sep  4 11:50:52 2022

@author: jenpopp
"""

from typing import cast

import seaborn as sns

# helmholtzcolors.py

helmholtz_information = "#a0235a"
helmholtz_health = "#D23264"
helmholtz_matter = "#F0781e"
helmholtz_energy = "#FFD228"
helmholtz_airspace = "#50C8aa"
helmholtz_environment = "#326469"

darkblue = "#0A2D6E"
helmholtzblue = "#175a9a"
blue60 = "#6691c2"
blue40 = "#cdd7eb"


grey = "#5A696E"
grey80 = "#78868b"
grey60 = "#99a5aa"
grey40 = "#bac3c7"

darkgreen = "#73951d"
helmholtzgreen = "#8CB423"
green60 = "#c4da8b"
green80 = "#aecd5e"


def set_plotstyle() -> None:
    sns.set_style("darkgrid", {"axes.facecolor": "#f2f0f0"})


def get_blues(n: int) -> list[tuple[float, float, float]]:
    blues = sns.blend_palette([darkblue, helmholtzblue, blue60, blue40], n)
    return cast(list[tuple[float, float, float]], blues)


def get_greens(n: int) -> list[tuple[float, float, float]]:
    greens = sns.blend_palette([darkgreen, helmholtzgreen, green60, "#dbeeaa"], n)
    return cast(list[tuple[float, float, float]], greens)


arraycolors131 = [helmholtzblue, grey40, grey60, grey80, helmholtzgreen]
arraycolors242 = [
    helmholtzblue,
    blue60,
    grey40,
    grey60,
    grey80,
    grey,
    green60,
    helmholtzgreen,
]
arraycolors232 = [
    helmholtzblue,
    blue60,
    grey40,
    grey60,
    grey80,
    green60,
    helmholtzgreen,
]
arraycolors151 = [helmholtzblue, grey40, grey60, grey80, grey, "k", helmholtzgreen]
arraycolors231 = [helmholtzblue, blue60, grey40, grey60, grey80, helmholtzgreen]
arraycolors222 = [helmholtzblue, blue60, grey40, grey60, green60, helmholtzgreen]
arraycolors123 = [helmholtzblue, grey40, grey60, green60, green80, helmholtzgreen]
arraycolors252 = [
    helmholtzblue,
    blue60,
    grey40,
    grey60,
    grey80,
    grey,
    "k",
    green60,
    helmholtzgreen,
]

arraycolors = {
    "B6": arraycolors131,
    "C1": arraycolors242,
    "C5": arraycolors232,
    "C10": arraycolors232,
    "C11": arraycolors232,
    "E4": arraycolors151,
    "E7a": arraycolors242,
    "E7b": arraycolors242,
    "I2": arraycolors242,
    "I3": arraycolors231,
    "D1": arraycolors222,
    "D2": arraycolors222,
    "D3": arraycolors123,
    "K2": arraycolors252,
    "K5": arraycolors242,
    "K9": arraycolors252,
    "K10": arraycolors242,
}
