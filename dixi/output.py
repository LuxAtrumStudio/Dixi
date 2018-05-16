import sys
import random
from dixi.input import getch
from dixi.color import get_color

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
    print(get_color(9, False, color) + "Error: " + msg + get_color('default', False, color))

def warning(msg, color):
    print(get_color(11, False, color) + "Warning: " + msg + get_color('default', False, color))

def success(msg, color):
    print(get_color(10, False, color) + "Success: " + msg + get_color('default', False, color))

def print_user(usr, color):
    random.seed(usr)
    random.randint(0, 256)
    rgb = (random.randint(0, 256), random.randint(0,256), random.randint(0, 256))
    if usr == 'Dixi' or usr == 'Admin':
        rgb = (128, 128, 128)
    return get_color(rgb, False, color) + usr + get_color('default', False, color)

