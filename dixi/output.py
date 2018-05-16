import os
import sys
import random
import math
from dixi.input import getch
from dixi.color import get_color
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

def prompt(name, description, color):
    if description is not str():
        description = '[' + get_color(15, False, color) + description + get_color(6, False, color) + ']'
    return input(get_color(6, False, color) + name + description + ': ' + get_color('default', False, color))

def prompt_secure(name, description, color):
    if description is not str():
        description = '[' + get_color(15, False, color) + description + get_color(6, False, color) + ']'
    print(get_color(6, False, color) + name + description + ': ' + get_color('default', False, color), end='')
    sys.stdout.flush()
    value = str()
    while True:
        ch = getch()
        if ord(ch) == 13:
            print()
            break
        elif ord(ch) == 127 and len(value) > 0:
            print("\033[D \033[D", end='')
            sys.stdout.flush()
            value = value[:-1]
        elif ord(ch) >= 33 and ord(ch) <= 126:
            print("*", end='')
            sys.stdout.flush()
            value += ch
    return value

def action(msg, color, verify=False):
    if not verify:
        print("\033[1m" + get_color(13, False, color) + msg + "\033[21m" + get_color('default', False, color))
    else:
        print("\033[1m" + get_color(13, False, color) + msg + "[Y/N]: \033[21m" + get_color('default', False, color), end='')
        sys.stdout.flush()
        yn = input()
        if(yn.lower() in ('y', 'yes')):
            return True
        else:
            return False

def error(msg, color):
    print(get_color(9, False, color) + "Error: " + msg.title() + get_color('default', False, color))

def warning(msg, color):
    print(get_color(11, False, color) + "Warning: " + msg.title() + get_color('default', False, color))

def success(msg, color):
    print(get_color(10, False, color) + "Success: " + msg.title() + get_color('default', False, color))

def print_user(usr, color):
    random.seed(usr)
    random.randint(0, 256)
    rgb = (random.randint(0, 256), random.randint(0,256), random.randint(0, 256))
    if usr == 'Dixi' or usr == 'Admin':
        rgb = (128, 128, 128)
    return get_color(rgb, False, color) + usr + get_color('default', False, color)

def print_message(data, longest, color, width=80):
    usr = print_user(data['author'], color)
    usr = usr + (' ' * (longest - len(data['author'])))
    body = render(data['body'], width - (longest + 2)).replace('\n', '\n' + (' ' * (longest + 2)))
    print(usr, end='  ')
    for line in body.split('\n'):
        print(line)

def print_channel(channel, color, width=80):
    print('\u250f', '\u2501' * (width - 2), '\u2513', sep='')
    print('\u2503', '\033[1m{:^{}}\033[0m'.format(channel, width - 2), '\u2503', sep='')
    print('\u2517', '\u2501' * (width - 2), '\u251b', sep='')

def print_set(items):
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
                print("{:{}}".format(li[i], width), end='')
            else:
                print(" " * (width + 3), end='')
        print('')

