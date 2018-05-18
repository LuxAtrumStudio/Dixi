import os
import sys
import json
import requests
import dixi.config
from dixi.input import getch, timeout
from dixi.pannel import Pannel
from dixi.output import prompt, prompt_secure, action, error, warning, success

def gen_card(name, lines):
    rows, columns = os.popen("stty size", "r").read().split()
    rows = int(rows)
    columns = int(columns)
    lines += 2
    card = Pannel('\033[1m{}\033[0m'.format(name), (lines, columns // 4), ((rows - lines) // 2, (columns - (columns // 4)) // 2))
    card.clear(True)
    card.render()
    return card

def create(color):
    card = gen_card("Create Channel", 4)
    title = str()
    while title is str():
        title = prompt(card, 'Title', '', color)
    if title is None:
        return
    users = prompt(card, 'Users', '', color)
    if users is None:
        return
    else:
        users = users.split(' ')
    action(card, 'Creating Channel {}'.format(title), color)
    response = requests.post('http://{}/channels/create'.format(dixi.config.get('addr')), data={'title': title, 'users': ','.join(users)}, cookies=dixi.config.get('cookies'))
    if 'error' in response:
        error(card, response['error'], color)
        timeout(dixi.config.get('timeout'))
    success(card, 'Created Channel {}'.format(title), color)
    timeout(dixi.config.get('timeout'))

def delete(color):
    card = gen_card("Delete Channel", 3)
    channel = str()
    while channel is str():
        channel = prompt(card, 'Channel', '', color)
    if channel is None:
        return
    if action(card, 'Delete Channel {}'.format(channel), color, True):
        response = requests.post('http://{}/channels/delete'.format(dixi.config.get('addr')), data={'title': channel}, cookies=dixi.config.get('cookies')).json()
        if 'error' in response:
            error(card, response['error'], color)
            timeout(dixi.config.get('timeout'))
            return
        success(card, 'Deleted Channel {}'.format(channel), color)
    timeout(dixi.config.get('timeout'))


def list():
    content = requests.get("http://{}/channels/list".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    if 'error' in content:
        return []
    return content['channels']

