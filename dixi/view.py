import sys
import json
import requests
import dixi.config
from dixi.output import *

def channels(args):
    action('Getting Channel List', args.color)
    content = requests.get("http://{}/channels/list".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    if 'error' in content:
        error(content['error'], args.color)
        sys.exit(3)
    print_set([" * {}".format(x) for x in content['channels']])

def users(args):
    action('Getting User List', args.color)
    content = requests.get("http://{}/users/list".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    current = content['current'] if 'current' in content else ''
    data = []
    for usr in content['users']:
        if usr == current:
            data.append('\033[1m * [{}]\033[0m'.format(print_user(usr, args.color)))
        else:
            data.append(' * {}'.format(print_user(usr, args.color)))
    print_set(data)

def view_post(args):
    response = dict()
    if args.channel:
        response = requests.get("http://{}/{}".format(dixi.config.get('addr'), args.channel), cookies=dixi.config.get('cookies')).json()
        if 'error' in response:
            error(response['error'], args.color)
            sys.exit(5)
        longest = max([len(x) for x in response['users']])
        print_channel(args.channel, args.color)
        for msg in response['messages']:
            print_message(msg, longest, args.color)
    else:
        response = requests.get("http://{}/".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
        if 'error' in response:
            error(response['error'], args.color)
            sys.exit(5)
        longest = max([len(x) for x in response['users']])
        for channel in response:
            if channel == 'users' or channel == 'update':
                continue
            print_channel(channel, args.color)
            for msg in response[channel]:
                print_message(msg, longest, args.color)
            print()

def post(args):
    response = requests.post('http://{}/{}/post'.format(dixi.config.get('addr'), args.channel), cookies=dixi.config.get('cookies'), data={'message': ' '.join(args.post)}).json()
    if 'error' in response:
        error(response['error'], args.color)
        sys.exit(6)
    success('Posted message to {}'.format(args.channel), args.color)
    print_message(response, len(response['author']), args.color)


def main(args):
    if args.channel == 'users':
        users(args)
    elif args.channel == 'channels':
        channels(args)
    else:
        print(args)
        if args.post == []:
            view_post(args)
        else:
            post(args)
