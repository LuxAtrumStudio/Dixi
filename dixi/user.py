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

def register(args, card=None):
    if card is None:
        while args.name is None or args.name is str():
            args.name = prompt('Username', '', args.color)
        while args.email is None or args.email is str():
            args.email = prompt('Email', 'Recovery email address', args.color)
        while args.password is None or args.password is str():
            args.password= prompt_secure('Password','', args.color)
        while args.password2 is None or args.password2 is str():
            args.password2= prompt_secure('Password Confirmation','', args.color)
        if args.password != args.password2:
            error('Passwords do not match', args.color)
            sys.exit(1)
        action('Registering User {}'.format(args.name), args.color)
        try:
            response = requests.post('http://{}/users/register'.format(dixi.config.get('addr')), data={'name': args.name, 'email': args.email, 'password': args.password, 'password2': args.password2}).json()
        except:
            response = {'error': "HTTP error"}
        if 'error' in response:
            error(response['error'], args.color)
            sys.exit(2)
        else:
            success('Created user {}'.format(args.name), args.color)
    else:
        color = args
        name = str()
        email = str()
        password = str()
        password2 = str()
        while name is str():
            name = prompt('Username', '', color, card)
        if name is None:
            return
        while email is str():
            email = prompt('Email', 'Recovery email address', color, card)
        if email is None:
            return
        while password is str():
            password= prompt_secure('Password','', color, card)
        if password is None:
            return
        while password2 is str():
            password2= prompt_secure('Password Confirmation','', color, card)
        if password2 is None:
            return
        if password != password2:
            error('Passwords do not match', color, card)
            timeout(dixi.config.get('timeout'))
            return
        action('Registering User {}'.format(name), color, card)
        try:
            response = requests.post('http://{}/users/register'.format(dixi.config.get('addr')), data={'name': name, 'email': email, 'password': password, 'password2': password2}).json()
        except:
            response = {'error': "Invalid url address"}
        if 'error' in response:
            error(response['error'], color, card)
            timeout(dixi.config.get('timeout'))
            return
        else:
            success('Created user {}'.format(name), color, card)
        timeout(dixi.config.get('timeout'))


def login(args, card=None):
    if card is None:
        while args.name is None or args.name is str():
            args.name = prompt('Username', '', args.color)
        while args.password is None or args.password is str():
            args.password= prompt_secure('Password','', args.color)
        action('Logging in {}'.format(args.name), args.color)
        try:
            response = requests.post('http://{}/users/login'.format(dixi.config.get('addr')), data={'username': args.name, 'password': args.password})
        except:
            response = {'error': "HTTP error"}
        if 'success' in response.json():
            success('Logged in {}'.format(args.name), args.color)
            dixi.config.set('cookies', dict(response.cookies))
    else:
        color = args
        name = str()
        password = str()
        while name is str():
            name = prompt('Username', '', color, card)
        if name is None:
            return
        while password is str():
            password= prompt_secure('Password','', color, card)
        if password is None:
            return
        action('Logging in {}'.format(name), color, card)
        try:
            response = requests.post('http://{}/users/login'.format(dixi.config.get('addr')), data={'username': name, 'password': password})
        except:
            response = {'error': 'Invalid url'}
        try:
            response.json()
        except:
            return
        if 'success' in response.json():
            success('Logged in {}'.format(name), color, card)
            dixi.config.set('cookies', dict(response.cookies))
            dixi.config.set('user', name)
        timeout(dixi.config.get('timeout'))

def logout(args, card=None):
    if card is None:
        if not action('Logout', args.color, True):
            sys.exit(0)
        dixi.config.set('cookies')
        success('Logged out', args.color)
    else:
        color= args
        card = gen_card("Logout", 2)
        if action('Logout', color, True, card):
            dixi.config.set('cookies')
            dixi.config.set('user')
            success('Logged out', color, card)
        else:
            warning('Not Logging Out', color, card)
        timeout(dixi.config.get('timeout'))

def delete(args, card=None):
    if card is None:
        if not action('Delete User {}'.format(args.name if args.name else 'Current'), args.color, True):
            sys.exit(0)
        try:
            if args.name:
                    response = requests.post('http://{}/users/delete'.format(dixi.config.get('addr')), data={'name': args.name}, cookies=dixi.config.get('cookies')).json()
            else:
                response = requests.get('http://{}/users/delete'.format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
        except:
            response = {'error': 'HTTP error'}
        if 'error' in response:
            error(response['error'], args.color)
            sys.exit(9)
        success('Deleted User {}'.format(args.name), args.color)
    else:
        color = args
        card = gen_card('Delete User', 3)
        name = prompt('Username', '', color, card)
        if name is None:
            return
        if not action('Delete User {}'.format(name if name else 'Current'), color, True, card):
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
            error(response['error'], color, card)
        else:
            success('Deleted User {}'.format(name), color, card)
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

def login_card(args):
    return login(args, gen_card("Login", 4))

def logout_card(args):
    return logout(args, gen_card("Logout", 2))

def register_card(args):
    return register(args, gen_card("Register", 6))

def delete_card(args):
    return delete(args, gen_card("Delete User", 3))

def main(args):
    if args.user_command == 'register':
        register(args)
    elif args.user_command == 'login':
        login(args)
    elif args.user_command == 'logout':
        logout(args)
    elif args.user_command == 'delete':
        delete(args)
