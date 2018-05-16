import sys
import json
import requests
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
    response = requests.post('http://10.0.0.17:3000/users/register', data={'name': args.name, 'email': args.email, 'password': args.password, 'password2': args.password2}).json()
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
    response = requests.post('http://10.0.0.17:3000/users/login', data={'username': args.name, 'password': args.password}).json()
    if 'success' in response:
        success('Logged in {}'.format(args.name), args.color)

def logout(args):
    if not action('Logout', args.color, True):
        sys.exit(0)

def delete(args):
    if not action('Delete User {}'.format(args.name if args.name else 'Current'), args.color, True):
        sys.exit(0)

def main(args):
    if args.user_command == 'register':
        register(args)
    elif args.user_command == 'login':
        login(args)
    elif args.user_command == 'logout':
        logout(args)
    elif args.user_command == 'delete':
        delete(args)
