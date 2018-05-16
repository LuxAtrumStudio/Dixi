import os
import sys
from enum import Enum

class Access(Enum):
    COLOR_0 = 0,
    COLOR_8 = 1,
    COLOR_16 = 2,
    COLOR_256 = 3,
    COLOR_TRUE = 4

def get_color_ability():
    if "COLORTERM" in os.environ:
        env = os.environ['COLORTERM']
        if env == "truecolor":
            return Access.COLOR_TRUE
    if "TERM" in os.environ:
        term = os.environ['TERM']
        if term == 'xterm':
            return Access.COLOR_256
        elif term == 'xterm-256color':
            return Access.COLOR_TRUE
        elif term == 'linux':
            return Access.COLOR_16
    return Access.COLOR_16

def clamp(color, minn, maxn):
    return max(minn, min(maxn, color))

def get_rgb(color):
    red = 0
    green = 0
    blue = 0
    if color < 232:
        for r in range(5):
            for g in range(5):
                for b in range(5):
                    if color == (36 * r) + (6 * g) + b + 16:
                        red = r / 5
                        green = g / 5
                        blue = b / 5
    else:
        color = color - 231
        red = (10 * color / 256)
        green = (10 * color / 256)
        blue = (10 * color / 256)
    return (red, green, blue)

def get_color_int(color, access, background):
    color = clamp(color, 0, 256)
    if color < 8:
        return ("\033[{}m".format(color + 40) if background else "\033[{}m".format(color + 30))
    elif color < 16:
        if access == Access.COLOR_8:
            color = color - 8
            return ("\033[{}m".format(color + 40) if background else "\033[{}m".format(color + 30))
        else:
            return ("\033[{}m".format(color + 92) if background else "\033[{}m".format(color + 82))
    else:
        base_8 = [(0,0,0), (0.5, 0,0), (0,0.5,0), (0.5, 0.5, 0), (0, 0, 0.5), (0.5, 0, 0.5), (0, 0.5, 0.5), (0.75, 0.75, 0.75)];
        base_light = [(0.5, 0.5, 0.5), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1) (0, 1, 1), (1, 1, 1)];
        if access == Access.COLOR_8:
            r, g, b = get_rgb(color)
            color = base_8.index(min(base_8, key=lambda x: abs(x[0]-r) + abs(x[1]-g) + abs(x[2] - b)));
            return ("\033[{}m".format(color + 40) if background else "\033[{}m".format(color + 30))
        elif access == Access.COLOR_16:
            base = base_8 + base_light
            color = base.index(min(base, key=lambda x: abs(x[0]-r) + abs(x[1]-g) + abs(x[2] - b)));
            if(color < 8):
                return ("\033[{}m".format(color + 40) if background else "\033[{}m".format(color + 30))
            else:
                return ("\033[{}m".format(color + 92) if background else "\033[{}m".format(color + 82))
        else:
            return ("\033[48;5;{}m".format(color) if background else "\033[38;5;{}m".format(color))


def get_color_rgb(color, access, background):
    red, green, blue = color
    red = clamp(red, 0, 256)
    green = clamp(green, 0, 256)
    blue = clamp(blue, 0, 256)
    if access != Access.COLOR_TRUE:
        red = ((red / 256) * 5)
        green = ((green / 256) * 5)
        blue = ((blue / 256) * 5)
        color = (36 * int(round(red))) + (6 * int(round(green))) + int(round(blue)) + 16
        return get_color_int(color, access, background)
    else:
        return ("\033[48;2;{};{};{}m".format(red, green, blue) if background else "\033[38;2;{};{};{}m".format(red, green, blue))

def get_color(color, background=False, enable_color=True):
    access = get_color_ability()
    if access == Access.COLOR_0 or enable_color == False:
        return ""
    if isinstance(color, str):
        if color.lower() == 'default':
            return ("\033[49m" if background else "\033[39m")
        color = color.lstrip('#')
        color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    if isinstance(color, list):
        color = tuple(color)
    if isinstance(color, tuple):
        return get_color_rgb(color, access, background)
    elif isinstance(color, int):
        return get_color_int(color, access, background)



