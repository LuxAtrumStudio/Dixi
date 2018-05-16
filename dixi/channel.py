import sys
from dixi.output import *

def create(args):
    while args.title is None or args.title is str():
        args.title = prompt('Title', '', args.color)
    if args.users == []:
        args.users = prompt('Users', '', args.color).split(',')
    action('Creating Channel {}'.format(args.title), args.color)

def delete(args):
    while args.channel is None or args.channel is list():
        args.title = prompt('Channel', '', args.color)
    if not action('Delete Channel {}'.format(args.title), args.color, True):
        sys.exit(0)


def main(args):
    if args.channel_command == 'create':
        create(args)
    elif args.channel_command == 'delete':
        delete(args)
