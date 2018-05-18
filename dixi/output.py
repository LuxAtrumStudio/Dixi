import os
import sys
import math
import dixi.rand as rand
from dixi.input import getch, getinput
from dixi.color import get_color, brighten
from dixi.markdown import render

def display_length(string):
    length = 0
    counting = 0
    for char in string:
        if char == '\033':
            counting = 1
        elif char == 'm' and counting == 1:
            counting = 0
            length -= 1
        if counting == 0:
            length += 1
    return length

def prompt(card, name, description, color):
    if description is not str():
        description = '[' + get_color(15, False, color) + description + get_color(6, False, color) + ']'
    card.print(get_color(6, False, color) + name + description + ': ' + get_color('default', False, color), end='')
    value = str()
    card.move_to((-1, 2))
    while True:
        ch = getch()
        if ord(ch) == 13:
            card.print()
            break
        elif ord(ch) == 127 and len(value) > 0:
            card.print("\033[D \033[D", end='')
            sys.stdout.flush()
            value = value[:-1]
        elif ord(ch) >= 33 and ord(ch) <= 126:
            card.print(ch, end='')
            sys.stdout.flush()
            value += ch
        elif ord(ch) == 27:
            card.print()
            return None
        card.move_to((-1, 2))
    return value

def prompt_choices(card, name, description, choices, color):
    if description is not str():
        description = '[' + get_color(15, False, color) + description + get_color(6, False, color) + ']'
    card.print(get_color(6, False, color) + name + description + ": " + get_color('default', False, color), end='')
    sel = 0
    card.move_to((-1, 2))
    while True:
        card.pop()
        card.print(get_color(6, False, color) + name + description + ": " + get_color('default', False, color), end='')
        for i, it in enumerate(choices):
            if i == sel:
                card.print("\033[7m" + str(it) + '\033[27m', end=' ')
            else:
                card.print(it, end=' ')
        ch = getinput()
        if ch == 'ENTER':
            card.print()
            break
        elif ch == 'RIGHT' and sel < len(choices) - 1:
            sel += 1
        elif ch == 'LEFT' and sel > 0:
            sel -= 1
        elif ch == 'ESCAPE':
            card.print()
            return None
    return choices[sel]


def prompt_secure(card, name, description, color):
    if description is not str():
        description = '[' + get_color(15, False, color) + description + get_color(6, False, color) + ']'
    card.print(get_color(6, False, color) + name + description + ': ' + get_color('default', False, color), end='')
    sys.stdout.flush()
    value = str()
    card.move_to((-1, 2))
    while True:
        ch = getch()
        if ord(ch) == 13:
            card.print()
            break
        elif ord(ch) == 127 and len(value) > 0:
            card.print("\033[D \033[D", end='')
            sys.stdout.flush()
            value = value[:-1]
        elif ord(ch) >= 33 and ord(ch) <= 126:
            card.print("*", end='')
            sys.stdout.flush()
            value += ch
        elif ord(ch) == 27:
            return None
        card.move_to((-1, 2))
    return value

def prompt_markdown(card, name, color):
    card.print(get_color(6, False, color) + name + ': ' + get_color('default', False, color))
    markdown = str()
    cnt = -1
    while True:
        ch = getch()
        if ord(ch) == 27:
            return markdown
        elif ord(ch) == 127 and len(markdown) > 0:
            markdown = markdown[:-1]
        elif ord(ch) == 13:
            if markdown[-1] == '\n':
                return markdown[:-1]
            markdown += '\n'
        elif ord(ch) >= 32 and ord(ch) <= 126:
            markdown += ch
        rend = render(markdown, 80, color)
        if cnt != -1:
            card.clear()
            card.print(get_color(6, False, color) + name + ': ' + get_color('default', False, color))
        card.print(rend)
        cnt = rend.count('\n')
    return markdown

def action(card, msg, color, verify=False):
    if not verify:
        card.print("\033[1m" + get_color(13, False, color) + msg + "\033[21m" + get_color('default', False, color))
    else:
        card.print("\033[1m" + get_color(13, False, color) + msg + "[Y/N]: \033[21m" + get_color('default', False, color), end='')
        yn = getch()
        card.print(yn)
        if (yn.lower() in ('y', 'yes')) or ord(yn) == 13:
            return True
        else:
            return False

def error(card, msg, color):
    card.print(get_color(9, False, color) + "Error: " + msg.title() + get_color('default', False, color))

def warning(card, msg, color):
    card.print(get_color(11, False, color) + "Warning: " + msg.title() + get_color('default', False, color))

def success(card, msg, color=False):
    card.print(get_color(10, False, color) + "Success: " + msg.title() + get_color('default', False, color))

def print_user(usr, color):
    rand.seed(usr)
    rgb = sorted([0, rand.rand(0, 256), rand.rand(0, 256), 256])
    rgb = [rgb[i+1] - rgb[i] for i in range(0, len(rgb) - 1)]
    rgb = brighten(rgb, 0.5)
    if usr == 'Dixi' or usr == 'Admin':
        rgb = (128, 128, 128)
    return get_color(rgb, False, color) + usr + get_color('default', False, color)

def print_message(card, data, longest, color):
    width = card.dim[1] - 2
    usr = print_user(data['author'], color)
    usr = usr + (' ' * (longest - len(data['author'])))
    body = render(data['body'], width - (longest + 2), color).replace('\n', '\n' + (' ' * (longest + 2)))
    card.print(usr, end='  ')
    for line in body.split('\n'):
        card.print(line)

def print_channel(card, channel, color, width=80):
    card.print('\u250f', '\u2501' * (width - 2), '\u2513', sep='')
    card.print('\u2503', '\033[1m{:^{}}\033[0m'.format(channel, width - 2), '\u2503', sep='')
    card.print('\u2517', '\u2501' * (width - 2), '\u251b', sep='')

def print_set(card, items):
    cp = items[:]
    rows, columns = os.popen("stty size", "r").read().split()
    rows = int(rows)
    columns = int(columns)
    lengths = [display_length(x) + 2 for x in cp]
    count = len(cp)
    col = 1
    while count / col > (rows * 0.25):
        col += 1
    while col * max(lengths) > columns:
        col -= 1
    width = max(lengths) - 2
    split = count / col
    groups = []
    last = 0.0
    while len(cp) % int(math.ceil(split)) != 0:
        cp.append(None)
    split = len(cp) / col
    while last < len(cp):
        groups.append(cp[int(last):int(last + split)])
        last += split
    for i in range(0, len(max(groups, key=len))):
        for li in groups:
            if len(li) > i and li[i] is not None:
                card.print("{:{}}".format(li[i], width), end='')
            else:
                card.print(" " * (width + 3), end='')
        card.print('')

