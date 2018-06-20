import os
import sys
import json
import requests
import dixi.config

from dixi.map import Map

from dixi.input import getch, timeout
from dixi.output import *
from dixi.pannel import Pannel

def gen_card(name, lines):
    rows, columns = os.popen("stty size", "r").read().split()
    rows = int(rows)
    columns = int(columns)
    lines += 2
    card = Pannel('\033[1m{}\033[0m'.format(name), (lines, columns // 4), ((rows - lines) // 2, (columns - (columns // 4)) // 2))
    card.clear(True)
    card.render()
    return card

def create(args, card=None):
    while args.title is str():
        args.title = prompt('Title', '', args.color, card)
    if args.title is None:
        return
    print(args)
    if args.users == []:
        args.users = prompt('Users', '', args.color, card)
    if args.users is None:
        return
    else:
        args.users = args.users.split(' ')
    action('Creating Channel {}'.format(args.title), args.color, card)
    try:
        response = requests.post('http://{}/channels/create'.format(dixi.config.get('addr')), data={'title': args.title, 'users': ','.join(args.users)}, cookies=dixi.config.get('cookies'))
    except:
        response = {'error': 'HTTP error'}
    if 'error' in response:
        error(response['error'], args.color, card)
        if card is None:
            sys.exit(4)
    else:
        success('Created Channel {}'.format(args.title), args.color, card)
    if card is not None:
        timeout(dixi.config.get('timeout'))

def delete(args, card=None):
    while args.channel is str():
        args.channel = prompt('Channel', '', args.color, card)
    if args.channel is None:
        return
    if action('Delete Channel {}'.format(args.channel), args.color, True, card):
        try:
            response = requests.post('http://{}/channels/delete'.format(dixi.config.get('addr')), data={'title': args.channel}, cookies=dixi.config.get('cookies')).json()
        except:
            response = {'error': 'Invalid url'}
        if 'error' in response:
            error(response['error'], args.color, card)
        else:
            success('Deleted Channel {}'.format(args.channel), args.color, card)
        if card is not None:
            timeout(dixi.config.get('timeout'))

def list():
    try:
        content = requests.get("http://{}/channels/list".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    except:
        return []
    if 'error' in content:
        return []
    return content['channels']

def create_card(args):
    return create(Map(users=[], title='', color=args), gen_card("Create Channel", 4))

def delete_card(args):
    return delete(Map(channel='', color=args), gen_card("Delete Channel", 3))
