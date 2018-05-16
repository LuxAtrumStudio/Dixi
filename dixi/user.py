import sys
import json
import requests
import dixi.config
from dixi.output import *

def register(args):
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
    response = requests.post('http://{}/users/register'.format(dixi.config.get('addr')), data={'name': args.name, 'email': args.email, 'password': args.password, 'password2': args.password2}).json()
    if 'error' in response:
        error(response['error'], args.color)
        sys.exit(2)
    else:
        success('Created user {}'.format(args.name), args.color)


def login(args):
    while args.name is None or args.name is str():
        args.name = prompt('Username', '', args.color)
    while args.password is None or args.password is str():
        args.password= prompt_secure('Password','', args.color)
    action('Logging in {}'.format(args.name), args.color)
    response = requests.post('http://{}/users/login'.format(dixi.config.get('addr')), data={'username': args.name, 'password': args.password})
    if 'success' in response.json():
        success('Logged in {}'.format(args.name), args.color)
        dixi.config.set('cookies', dict(response.cookies))

def logout(args):
    if not action('Logout', args.color, True):
        sys.exit(0)
    dixi.config.set('cookies')
    success('Logged out', args.color)

def delete(args):
    if not action('Delete User {}'.format(args.name if args.name else 'Current'), args.color, True):
        sys.exit(0)
    if args.name:
        response = requests.post('http://{}/users/delete'.format(dixi.config.get('addr')), data={'name': args.name}, cookies=dixi.config.get('cookies')).json()
    else:
        response = requests.get('http://{}/users/delete'.format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    if 'error' in response:
        error(response['error'], args.color)
        sys.exit(9)
    success('Deleted User {}'.format(args.name), args.color)

def main(args):
    if args.user_command == 'register':
        register(args)
    elif args.user_command == 'login':
        login(args)
    elif args.user_command == 'logout':
        logout(args)
    elif args.user_command == 'delete':
        delete(args)
