import sys
import json
import requests
import dixi.config
from dixi.output import *

def create(args):
    while args.title is None or args.title is str():
        args.title = prompt('Title', '', args.color)
    if args.users == []:
        args.users = prompt('Users', '', args.color).split(' ')
    action('Creating Channel {}'.format(args.title), args.color)
    response = requests.post('http://{}/channels/create'.format(dixi.config.get('addr')), data={'title': args.title, 'users': ','.join(args.users)}, cookies=dixi.config.get('cookies'))
    if 'error' in response:
        error(response['error'], args.color)
        sys.exit(4)
    success('Created Channel {}'.format(args.title), args.color)

def delete(args):
    while args.channel is None or args.channel is str():
        args.channel = prompt('Channel', '', args.color)
    if not action('Delete Channel {}'.format(args.channel), args.color, True):
        sys.exit(0)


def main(args):
    if args.channel_command == 'create':
        create(args)
    elif args.channel_command == 'delete':
        delete(args)
