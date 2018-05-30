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


def register(color):
    card = gen_card("Register", 6)
    name = str()
    email = str()
    password = str()
    password2 = str()
    while name is str():
        name = prompt(card, 'Username', '', color)
    if name is None:
        return
    while email is str():
        email = prompt(card, 'Email', 'Recovery email address', color)
    if email is None:
        return
    while password is str():
        password= prompt_secure(card, 'Password','', color)
    if password is None:
        return
    while password2 is str():
        password2= prompt_secure(card, 'Password Confirmation','', color)
    if password2 is None:
        return
    if password != password2:
        error(card, 'Passwords do not match', color)
        timeout(dixi.config.get('timeout'))
        return
    action(card, 'Registering User {}'.format(name), color)
    try:
        response = requests.post('http://{}/users/register'.format(dixi.config.get('addr')), data={'name': name, 'email': email, 'password': password, 'password2': password2}).json()
    except:
        response = {'error': "Invalid url address"}
    if 'error' in response:
        error(card, response['error'], color)
        timeout(dixi.config.get('timeout'))
        return
    else:
        success(card, 'Created user {}'.format(name), color)
    timeout(dixi.config.get('timeout'))


def login(color):
    card = gen_card("Login", 4)
    name = str()
    password = str()
    while name is str():
        name = prompt(card, 'Username', '', color)
    if name is None:
        return
    while password is str():
        password= prompt_secure(card, 'Password','', color)
    if password is None:
        return
    action(card, 'Logging in {}'.format(name), color)
    try:
        response = requests.post('http://{}/users/login'.format(dixi.config.get('addr')), data={'username': name, 'password': password})
    except:
        response = {'error': 'Invalid username or url'}
    if 'success' in response.json():
        success(card, 'Logged in {}'.format(name), color)
        dixi.config.set('cookies', dict(response.cookies))
        dixi.config.set('user', name)
    timeout(dixi.config.get('timeout'))

def logout(color):
    card = gen_card("Logout", 2)
    if action(card, 'Logout', color, True):
        dixi.config.set('cookies')
        dixi.config.set('user')
        success(card, 'Logged out', color)
    else:
        warning(card, 'Not Logging Out', color)
    timeout(dixi.config.get('timeout'))

def delete(color):
    card = gen_card('Delete User', 3)
    name = prompt(card, 'Username', '', color)
    if name is None:
        return
    if not action(card, 'Delete User {}'.format(name if name else 'Current'), color, True):
        sys.exit(0)
    if name:
        try:
            response = requests.post('http://{}/users/delete'.format(dixi.config.get('addr')), data={'name': name}, cookies=dixi.config.get('cookies')).json()
        except:
            response = {'error': 'Invalid url'}
    else:
        try:
            response = requests.get('http://{}/users/delete'.format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
        except:
            response = {'error': 'Invalid url'}
    if 'error' in response:
        error(card, response['error'], color)
    else:
        success(card, 'Deleted User {}'.format(name), color)
        if name == dixi.config.get('user'):
            dixi.config.set('user')
    timeout(dixi.config.get('timeout'))

def list():
    try:
        content = requests.get("http://{}/users/list".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    except:
        return []
    return content['users']

def current():
    try:
        content = requests.get("http://{}/users/current".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    except requests.exceptions.RequestException as ex:
        return False
    return content['loggedin']
