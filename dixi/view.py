import sys
import json
import requests
from dixi.output import *

def channels(args):
    action('Getting Channel List', args.color)

def users(args):
    action('Getting User List', args.color)
    content = requests.get("http://10.0.0.17:3000/users/list").json()
    current = content['current'] if 'current' in content else ''
    for usr in content['users']:
        if usr == current:
            print('\033[1m *', print_user(usr, args.color), "<<\033[0m")
        else:
            print(" *", print_user(usr, args.color))

def post(args):
    pass

def main(args):
    if args.group == 'users':
        users(args)
    elif args.group == 'channels':
        channels(args)
    else:
        post(args)
