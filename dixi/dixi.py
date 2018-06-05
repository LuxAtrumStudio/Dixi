import argparse
import os
import sys

import dixi.config
import dixi.user
import dixi.channel
import dixi.view
import dixi.markdown
from dixi.color import get_color
from dixi.output import print_user, print_message, display_length
from dixi.input import getinput, timeout

from dixi.pannel import Pannel

rows, columns = os.popen("stty size", "r").read().split()
rows = int(rows)
columns = int(columns)

PANNELS = {
        'menu': {
            'pannel': Pannel('\033[1mDIXI\033[0m', (3, columns - 2), (1, 1)),
            'options': [],
            'selection': 0,
            'endchar': ''
            },
        'channels': {
            'pannel': Pannel('\033[1mChannels\033[0m', ((rows - 5) // 2, 15), (4, 1)),
            'options': [],
            'selection': 0,
            'endchar': '\n'
            },
        'users': {
            'pannel': Pannel("\033[1mUsers\033[0m", ((rows - 5) // 2, 15), (4 + ((rows - 5) // 2), 1)),
            'options': [],
            'selection': -1,
            'endchar': '\n'
            },
        'main':{
            'pannel': Pannel('', (rows - 2 - 3 - 7, columns - 2 - 15), (4, 16)),
            },
        'entry': {
            'pannel': Pannel('', (7, columns - 2 - 15), (rows - 8, 16))
            }
        }

POSTS = {}

CHANNELS = {}

pannel = 'entry'
longest = 0
current_channel = None
body = str()


def clear_term():
    rows, columns = os.popen("stty size", "r").read().split()
    rows = int(rows)
    columns = int(columns)
    print('\033[H', end='')
    for i in range(rows):
        print('\033[2K')
    print('\033[H', end='')

def resize_pannels():
    global PANNELS
    global rows, columns
    global current_channel
    trows, tcolumns = os.popen("stty size", "r").read().split()
    trows = int(trows)
    tcolumns = int(tcolumns)
    if trows != rows or tcolumns != columns:
        rows = trows
        columns = tcolumns
    else:
        return
    clear_term()
    PANNELS['menu']['pannel'].resize((3, columns - 2))
    PANNELS['menu']['pannel'].move((1,1))
    PANNELS['channels']['pannel'].resize(((rows - 5) // 2, 15))
    PANNELS['channels']['pannel'].move((4,1))
    PANNELS['users']['pannel'].resize(((rows - 5) // 2, 15))
    PANNELS['users']['pannel'].move((4 + ((rows - 5) // 2),1))
    PANNELS['main']['pannel'].resize((rows - 2 - 3- 7, columns - 2 - 15))
    PANNELS['main']['pannel'].move((4, 16))
    PANNELS['main']['pannel'].resize((rows - 2 - 3- 7, columns - 2 - 15))
    PANNELS['main']['pannel'].move((4, 16))
    PANNELS['entry']['pannel'].resize((7, columns - 2 - 15))
    PANNELS['entry']['pannel'].move((rows - 8, 16))
    for key, val in PANNELS.items():
        val['pannel'].init = True
        val['pannel'].render()
    current_channel = -1
    display_channel()


def close():
    clear_term()
    dixi.config.set('update')
    dixi.config.save_config()
    sys.exit(0)


def write_options(pannel):
    global PANNELS
    global CHANNELS
    PANNELS[pannel]['pannel'].clear()
    for i, opt in enumerate(PANNELS[pannel]['options']):
        fmt = '{}'
        if PANNELS[pannel]['endchar'] == '':
            width = PANNELS[pannel]['pannel'].dim[1] // len(PANNELS[pannel]['options'])
            fmt = (' ' * ((width - len(opt)) // 2)) + fmt
            fmt += (' ' * (width - (len(fmt) - 2 + len(opt) + 2)))
        elif pannel == 'channels':
            if opt in CHANNELS and CHANNELS[opt] is False:
                fmt = ' ' + get_color(10, False, dixi.config.get('color')) + '\u25cf' + get_color('default', False, dixi.config.get('color')) + ' {}'
            else:
                fmt = '   {}'
        if i == PANNELS[pannel]['selection']:
            PANNELS[pannel]['pannel'].print(fmt.format("\033[7m" + opt + "\033[27m"), end=PANNELS[pannel]['endchar'])
        else:
            PANNELS[pannel]['pannel'].print(fmt.format(opt), end=PANNELS[pannel]['endchar'])

def load_posts():
    global POSTS
    global CHANNELS
    global current_channel
    if not dixi.config.get('update'):
        POSTS = {}
    posts, users, update = dixi.view.posts(dixi.config.get('color'), dixi.config.get('update'))
    for key, value in posts.items():
        if value and key != current_channel:
            CHANNELS[key] = False
        elif value and key == current_channel:
            current_channel = None
        if key in POSTS:
            POSTS[key] += value
        else:
            POSTS[key] = value
    load_channel()
    dixi.config.set('update', update)

def load_menu():
    global PANNELS
    current_user = dixi.config.get('user')
    if current_user:
        PANNELS['menu']['options'] = ['Logout', 'Delete', 'Create Channel', 'Delete Channel', 'Config', 'Quit']
    else:
        PANNELS['menu']['options'] = ['Login', 'Register', 'Config', 'Quit']
    PANNELS['menu']['selection'] = 0
    write_options('menu')

def load_channel():
    global PANNELS
    global CHANNELS
    if dixi.config.get('user'):
        channels = dixi.channel.list()
    else:
        channels = ["No channels available for {}".format(dixi.config.get('user'))]
    PANNELS['channels']['options'] = channels
    write_options('channels')

def load_user():
    global PANNELS
    global longest
    users = sorted(dixi.user.list())
    if(users):
        longest = len(max(users, key=len))
    else:
        longest = 0
    if dixi.config.get('user'):
        current = users.index(dixi.config.get('user'))
    else:
        current = -10000
    users = [" " + print_user(x, dixi.config.get('color')) if x != dixi.config.get('user') else '\033[1m[' + print_user(x, dixi.config.get('color')) + ']\033[0m' for x in users]
    PANNELS['users']['options'] = users
    write_options('users')
    PANNELS['users']['pannel'].cursor_set(0)
    last = -1
    while current - PANNELS['users']['pannel'].cursor > PANNELS['users']['pannel'].dim[0] - (PANNELS['users']['pannel'].dim[0] // 2) and last != PANNELS['users']['pannel'].cursor:
        last = PANNELS['users']['pannel'].cursor
        PANNELS['users']['pannel'].cursor_down()

def load():
    if not dixi.user.current():
        dixi.config.set('user')
        dixi.config.set('cookies')
    load_menu()
    load_posts()
    load_channel()
    load_user()
    if dixi.config.get('user'):
        PANNELS['entry']['pannel'].set_title(print_user(dixi.config.get('user'), dixi.config.get('color')))
    else:
        PANNELS['entry']['pannel'].set_title('')

def move_select(key):
    global PANNELS
    global pannel
    if 'selection' in PANNELS[pannel] and PANNELS[pannel]['selection'] != -1:
        if PANNELS[pannel]['endchar'] == '':
            if key == 'RIGHT' and PANNELS[pannel]['selection'] != len(PANNELS[pannel]['options']) - 1:
                PANNELS[pannel]['selection'] += 1
            elif key == 'LEFT' and PANNELS[pannel]['selection'] > 0:
                PANNELS[pannel]['selection'] -= 1
        elif PANNELS[pannel]['endchar'] == '\n':
            if key == 'DOWN' and PANNELS[pannel]['selection'] != len(PANNELS[pannel]['options']) - 1:
                PANNELS[pannel]['selection'] += 1
            elif key == 'UP' and PANNELS[pannel]['selection'] > 0:
                PANNELS[pannel]['selection'] -= 1
        write_options(pannel)

def move_main(key):
    global PANNELS
    if key.startswith('SHIFT_'):
        key = key[6:]
    if key == "UP":
        PANNELS['main']['pannel'].cursor_up()
    elif key == "DOWN":
        PANNELS['main']['pannel'].cursor_down()

def move_user(key):
    global PANNELS
    if key.startswith('CTRL_'):
        key = key[5:]
    if key == "UP":
        PANNELS['users']['pannel'].cursor_up()
    elif key == "DOWN":
        PANNELS['users']['pannel'].cursor_down()

def move_channel(key):
    global PANNELS
    if key.startswith('ALT_'):
        key = key[4:]
    if key == "UP":
        PANNELS['channels']['pannel'].cursor_up()
    elif key == "DOWN":
        PANNELS['channels']['pannel'].cursor_down()

def move(key):
    global PANNELS
    global pannel
    if key is None:
        return
    PANNELS[pannel]['pannel'].toggle_bold()
    if key == 'ESCAPE':
        if pannel == 'menu':
            pannel = 'entry'
        else:
            pannel = 'menu'
    elif key == 'TAB':
        PANNELS['channels']['selection'] += 1
        if PANNELS['channels']['selection'] > (PANNELS['channels']['pannel'].dim[0] // 2):
            PANNELS['channels']['pannel'].cursor_down()
        if PANNELS['channels']['selection'] == len(PANNELS['channels']['options']):
            PANNELS['channels']['selection'] = 0
            PANNELS['channels']['pannel'].cursor_set(0)
        write_options('channels')
    elif key == 'q' and pannel != 'entry':
        close()
    elif key.startswith("SHIFT_"):
        move_main(key)
    elif key.startswith("CTRL_"):
        move_user(key)
    elif key.startswith("ALT_"):
        move_channel(key)
    move_select(key)
    PANNELS[pannel]['pannel'].toggle_bold()

def action(key):
    global PANNELS
    global POSTS
    global CHANNELS
    global pannel
    clean = False
    if 'options' in PANNELS[pannel] and PANNELS[pannel]['selection'] != -1:
        clean = True
        option = PANNELS[pannel]['options'][PANNELS[pannel]['selection']]
        if option == 'Login':
            dixi.user.login(dixi.config.get('color'))
        elif option == 'Register':
            dixi.user.register(dixi.config.get('color'))
        elif option == 'Logout':
            dixi.user.logout(dixi.config.get('color'))
        elif option == 'Delete':
            dixi.user.delete(dixi.config.get('color'))
        elif option == 'Config':
            dixi.config.addr(dixi.config.get('color'))
            global current_channel
            current_channel = None
        elif option == 'Create Channel':
            dixi.channel.create(dixi.config.get('color'))
        elif option == 'Delete Channel':
            dixi.channel.delete(dixi.config.get('color'))
        elif option == 'Quit':
            close()
        load()

    if clean:
        clear_term()
        for key, value in PANNELS.items():
            value['pannel'].init = True

def display_channel():
    global PANNELS
    global CHANNELS
    global POSTS
    global longest
    global current_channel
    if PANNELS['channels']['selection'] >= len(PANNELS['channels']['options']):
        channel = -1
        PANNELS['main']['pannel'].clear(True)
        PANNELS['main']['pannel'].render_box()
        PANNELS['main']['pannel'].render_title()
        return
    else:
        channel = PANNELS['channels']['options'][PANNELS['channels']['selection']]
    if current_channel == channel:
        return
    if channel in CHANNELS and CHANNELS[channel] is False:
        CHANNELS[channel] = True
    PANNELS['main']['pannel'].clear(True)
    current_channel = channel
    if channel != 'No channels available for None':
        PANNELS['main']['pannel'].set_title(channel)
    else:
        PANNELS['main']['pannel'].set_title(None)
    if channel in POSTS:
        for post in POSTS[channel]:
            print_message(PANNELS['main']['pannel'], post, longest, dixi.config.get('color'))
        PANNELS['main']['pannel'].cursor_set(0)
        PANNELS['main']['pannel'].cursor_down(len(PANNELS['main']['pannel'].get_display()))

def message(key):
    global PANNELS
    global body
    global current_channel
    if key == 'DELETE':
        body = str()
    elif key == 'BACKSPACE' and len(body) > 0:
        body = body[:-1]
    elif key == 'ENTER':
        if body and body[-1] == '\n':
            if dixi.view.post_message(dixi.config.get('color'), body[:-1].lstrip(), PANNELS['main']['pannel'].title):
                load_posts()
                current_channel = None
                body = str()
            clear_term()
            for key, value in PANNELS.items():
                value['pannel'].init = True
        else:
            PANNELS['entry']['pannel'].cursor_down()
            body += '\n'
    elif len(key) == 1 and ord(key) >= 32 and ord(key) <= 126:
        body += key
    elif key == 'UP':
        PANNELS['entry']['pannel'].cursor_up()
    elif key == 'DOWN':
        PANNELS['entry']['pannel'].cursor_down()
    rend = dixi.markdown.render(body, PANNELS['entry']['pannel'].dim[1] - 2, dixi.config.get('color'))
    PANNELS['entry']['pannel'].clear(True)
    PANNELS['entry']['pannel'].print(rend)
    PANNELS['entry']['pannel'].render_box()
    PANNELS['entry']['pannel'].render_title()

def main():
    global PANNELS
    global pannel
    clear_term()
    dixi.config.load_config()
    PANNELS[pannel]['pannel'].toggle_bold()
    PANNELS['entry']['pannel'].toggle_cursor()
    PANNELS['entry']['pannel'].cursor_down()
    PANNELS['main']['pannel'].toggle_cursor()
    PANNELS['main']['pannel'].scroll = 1
    PANNELS['users']['pannel'].toggle_cursor()
    PANNELS['users']['pannel'].scroll = 1
    PANNELS['channels']['pannel'].toggle_cursor()
    PANNELS['channels']['pannel'].scroll = 1
    load()
    while True:
        resize_pannels()
        display_channel()
        for key, val in PANNELS.items():
            val['pannel'].render()
        PANNELS['entry']['pannel'].move_to((6, 2))
        key = getinput(10)
        if key is None:
            load_posts()
        if key == 'ENTER':
            action(key)
        else:
            move(key)
        if key is not None and pannel == 'entry':
            message(key)
    close()
