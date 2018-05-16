import os
import sys
import json

CONFIG = dict()

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
    load_config()
    if name in CONFIG:
        return CONFIG[name]
    return None

def exists(name):
    global CONFIG
    load_config()
    if name in CONFIG:
        return True
    return False

def set(name, value=None):
    global CONFIG
    load_config()
    CONFIG[name] = value
    save_config()

def main(args):
    if args.addr:
        set('addr', args.addr)
