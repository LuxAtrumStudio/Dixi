import argparse
import os
import sys

import dixi.config
import dixi.user
import dixi.channel
# import dixi.view
from dixi.output import print_user
from dixi.input import getinput

from dixi.pannel import Pannel

rows, columns = os.popen("stty size", "r").read().split()
rows = int(rows)
columns = int(columns)

PANNELS = {
        'menu': {
            'pannel': Pannel('\033[1mDIXI\033[0m', (3, columns - 2), (1, 1)),
            'options': [],
            'selection': 0,
            'endchar': ' '
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
            'pannel': Pannel('', (rows - 2 - 3 - 5, columns - 2 - 15), (4, 16)),
            },
        'entry': {
            'pannel': Pannel('', (5, columns - 2 - 15), (rows - 6, 16))
            }
        }
pannel = 'entry'

def write_options(pannel):
    global PANNELS
    PANNELS[pannel]['pannel'].clear()
    for i, opt in enumerate(PANNELS[pannel]['options']):
        if i == PANNELS[pannel]['selection']:
            PANNELS[pannel]['pannel'].print("\033[7m" + opt + "\033[0m", end=PANNELS[pannel]['endchar'])
        else:
            PANNELS[pannel]['pannel'].print(opt, end=PANNELS[pannel]['endchar'])

def load_menu():
    global PANNELS
    current_user = dixi.config.get('user')
    if current_user:
        PANNELS['menu']['options'] = ['Logout', 'Delete', 'Config', 'Quit']
    else:
        PANNELS['menu']['options'] = ['Login', 'Register', 'Config', 'Quit']
    write_options('menu')

def load_channel():
    global PANNELS
    if dixi.config.get('user'):
        channels = dixi.channel.list()
    else:
        channels = ["No channels available for {}".format(dixi.config.get('user'))]
    PANNELS['channels']['options'] = channels
    write_options('channels')

def load_user():
    global PANNELS
    users = [" " + print_user(x, True) if x != dixi.config.get('user') else '\033[1m[' + print_user(x, True) + ']\033[0m' for x in dixi.user.list()]
    PANNELS['users']['options'] = users
    write_options('users')

def load():
    if not dixi.user.current():
        dixi.config.set('user')
        dixi.config.set('cookies')
    load_menu()
    load_channel()
    load_user()
    if dixi.config.get('user'):
        PANNELS['entry']['pannel'].set_title(print_user(dixi.config.get('user'), True))
    else:
        PANNELS['entry']['pannel'].set_title('')

def move_select(key):
    global PANNELS
    global pannel
    if 'selection' in PANNELS[pannel] and PANNELS[pannel]['selection'] != -1:
        if PANNELS[pannel]['endchar'] == ' ':
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

def move(key):
    global PANNELS
    global pannel
    PANNELS[pannel]['pannel'].toggle_bold()
    if key == 'ESCAPE':
        if pannel == 'menu':
            pannel = 'entry'
        else:
            pannel = 'menu'
    elif key == 'q':
        print('\033[2J')
        dixi.config.save_config()
        sys.exit(0)
    move_select(key)
    PANNELS[pannel]['pannel'].toggle_bold()

def action(key):
    global PANNELS
    global pannel
    clean = False
    if 'options' in PANNELS[pannel] and PANNELS[pannel]['selection'] != -1:
        clean = True
        option = PANNELS[pannel]['options'][PANNELS[pannel]['selection']]
        if option == 'Login':
            dixi.user.login(True)
            load()
        elif option == 'Register':
            dixi.user.register(True)
            load()
        elif option == 'Logout':
            dixi.user.logout(True)
            load()
        elif option == 'Delete':
            dixi.user.delete(True)
            load()
        elif option == 'Config':
            dixi.config.addr(True)
            load()
        elif option == 'Quit':
            print('\033[2J')
            dixi.config.save_config()
            sys.exit(0)

    if clean:
        print('\033[2J', end='')
        for key, value in PANNELS.items():
            value['pannel'].init = True


def main():
    global PANNELS
    global pannel
    print('\033[2J', end='')
    dixi.config.load_config()
    load()
    PANNELS[pannel]['pannel'].toggle_bold()
    while True:
        for key, val in PANNELS.items():
            val['pannel'].render()
        key = getinput()
        if key == 'ENTER':
            action(key)
        else:
            move(key)

    # while True:
    #     for key, val in pannels.items():
    #         if key in options:
    #             endch = '\n'
    #             if key == 'menu':
    #                 endch = ' '
    #             val.clear()
    #             for i, op in enumerate(options[key]):
    #                 if i == selection[key]:
    #                     val.print('\033[7m' + op + '\033[27m', end=endch)
    #                 else:
    #                     val.print(op, end=endch)
    #         val.render()
    #     pannels['entry'].move_to((2,2))
    #     key = getinput()
    #     if key == 'q':
    #         break
    #     elif key == 'ESCAPE':
    #         pannels[pannel].toggle_bold()
    #         if pannel != 'menu':
    #             pannel = 'menu'
    #         else:
    #             pannel = 'entry'
    #         pannels[pannel].toggle_bold()
    #     elif key.startswith('CTRL_'):
    #         pannels[pannel].toggle_bold()
    #         pannel = move(key, pannel)
    #         pannels[pannel].toggle_bold()
    #     elif pannel == 'menu':
    #         if key == 'RIGHT' and selection[pannel] < len(options[pannel]) - 1:
    #             selection[pannel] += 1
    #         elif key == 'LEFT' and selection[pannel] > 0:
    #             selection[pannel] -= 1
    #         elif key == 'ENTER':
    #             menu_select(selection[pannel], options[pannel])
    #             print('\033[2J', end='')
    #             for key, val in pannels.items():
    #                 val.init = True
    #     elif pannel == 'side':
    #         if key == 'UP' and selection[pannel] > 0:
    #             selection[pannel] -= 1
    #         elif key == 'DOWN' and selection[pannel] < len(options[pannel]) - 1:
    #             selection[pannel] += 1
    #     pannels['main'].print(key)
    dixi.config.save_config()
    print('\033[2J')
