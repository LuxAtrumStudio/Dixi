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
    while email is str():
        email = prompt(card, 'Email', 'Recovery email address', color)
    while password is str():
        password= prompt_secure(card, 'Password','', color)
    while password2 is str():
        password2= prompt_secure(card, 'Password Confirmation','', color)
    if password != password2:
        error(card, 'Passwords do not match', color)
        sys.exit(1)
    action(card, 'Registering User {}'.format(name), color)
    response = requests.post('http://{}/users/register'.format(dixi.config.get('addr')), data={'name': name, 'email': email, 'password': password, 'password2': password2}).json()
    if 'error' in response:
        error(card, response['error'], color)
        sys.exit(2)
    else:
        success(card, 'Created user {}'.format(name), color)
    timeout(2)


def login(color):
    card = gen_card("Login", 4)
    name = str()
    password = str()
    while name is str():
        name = prompt(card, 'Username', '', color)
    while password is str():
        password= prompt_secure(card, 'Password','', color)
    action(card, 'Logging in {}'.format(name), color)
    response = requests.post('http://{}/users/login'.format(dixi.config.get('addr')), data={'username': name, 'password': password})
    if 'success' in response.json():
        success(card, 'Logged in {}'.format(name), color)
        dixi.config.set('cookies', dict(response.cookies))
        dixi.config.set('user', name)
    timeout(2)

def logout(color):
    card = gen_card("Logout", 2)
    if not action(card, 'Logout', color, True):
        sys.exit(0)
    dixi.config.set('cookies')
    dixi.config.set('user')
    success(card, 'Logged out', color)
    timeout(2)

def delete(color):
    card = gen_card('Delete', 3)
    name = prompt(card, 'Username', '', color)
    if not action(card, 'Delete User {}'.format(name if name else 'Current'), color, True):
        sys.exit(0)
    if name:
        response = requests.post('http://{}/users/delete'.format(dixi.config.get('addr')), data={'name': name}, cookies=dixi.config.get('cookies')).json()
    else:
        response = requests.get('http://{}/users/delete'.format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    if 'error' in response:
        error(card, response['error'], color)
        sys.exit(9)
    success(card, 'Deleted User {}'.format(name), color)
    if name == dixi.config.get('user'):
        dixi.config.set('user')
    timeout(2)

def list():
    content = requests.get("http://{}/users/list".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    return content['users']

def current():
    content = requests.get("http://{}/users/current".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    return content['loggedin']
