import os
import sys
import json
from dixi.pannel import Pannel
from dixi.input import timeout
from dixi.output import *

CONFIG = dict()

def gen_card(name, lines):
    rows, columns = os.popen("stty size", "r").read().split()
    rows = int(rows)
    columns = int(columns)
    lines += 2
    card = Pannel('\033[1m{}\033[0m'.format(name), (lines, columns // 4), ((rows - lines) // 2, (columns - (columns // 4)) // 2))
    card.clear(True)
    card.render()
    return card

def load_config():
    global CONFIG
    if CONFIG == dict():
        path = str()
        if os.path.exists(os.path.expanduser('~/.config/dixi/config')):
            path = '~/.config/dixi/config'
        elif os.path.exists(os.path.expanduser('~/.dixi/config')):
            path = '~/.dixi/config'
        elif os.path.exists(os.path.expanduser('~/.dixi')):
            path = '~/.dixi'
        path = os.path.expanduser(path)
        if path != '':
            with open(path) as file:
                CONFIG = json.load(file)

def save_config():
    global CONFIG
    if CONFIG != dict():
        if os.path.exists(os.path.expanduser('~/.config/dixi/config')):
            path = '~/.config/dixi/config'
        elif os.path.exists(os.path.expanduser('~/.dixi/config')):
            path = '~/.dixi/config'
        elif os.path.exists(os.path.expanduser('~/.dixi')):
            path = '~/.dixi'
        else:
            path = '~/.config/dixi/config'
        path= os.path.expanduser(path)
        if not os.path.exists(path):
            os.makedirs(os.path.split(path)[0])
        with open(path, 'w') as file:
            json.dump(CONFIG, file)

def get(name):
    global CONFIG
    if name in CONFIG:
        return CONFIG[name]
    return None

def exists(name):
    global CONFIG
    if name in CONFIG:
        return True
    return False

def set(name, value=None):
    global CONFIG
    CONFIG[name] = value

def addr(color):
    card = gen_card('Address', 5)
    addr = str()
    addr = prompt(card, 'Address', '', color)
    set_color = prompt_choices(card, 'Color', '', [True, False], color)
    post_prompt = prompt_choices(card, 'Post Prompt', '', [True, False], color)
    timeout_time = prompt_choices(card, 'Pause Delay', '', [-1, 0, 1, 2, 3, 4, 5], color)
    if addr and addr != str():
        set('addr', addr)
    if set_color is not None:
        set('color', set_color)
    if post_prompt is not None:
        set('post-prompt', post_prompt)
    if timeout_time is not None:
        if timeout_time == -1:
            timeout_time = 0
        elif timeout_time == 0:
            timeout_time = 0.005
        set('timeout', timeout_time)
    success(card, 'Set Dixi configuration', color)
    timeout(get('timeout'))
