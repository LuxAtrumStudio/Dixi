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
    if len(content['channels']) == 0:
        warning('no channels available to user', args.color)
    else:
        print_set([" \u25cf {}".format(x) for x in content['channels']])

def users(args):
    action('Getting User List', args.color)
    content = requests.get("http://{}/users/list".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    current = content['current'] if 'current' in content else ''
    data = []
    for usr in sorted(content['users']):
        if usr == current:
            data.append('\033[1m \u25cf [{}]\033[0m'.format(print_user(usr, args.color)))
        else:
            data.append(' \u25cf {}'.format(print_user(usr, args.color)))
    if (len(data) == 0):
        warning('no users', args.color)
    else:
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
        if len(response) == 2:
            warning('no posts on channels', args.color)
            return
        longest = max([len(x) for x in response['users']])
        for channel in response:
            if channel == 'users' or channel == 'update':
                continue
            print_channel(channel, args.color)
            for msg in response[channel]:
                print_message(msg, longest, args.color)
            print()

def post(args):
    if args.body == []:
        args.body = prompt_markdown('Message', args.color).split(' ')
        print(repr(args.body))
    response = requests.post('http://{}/{}/post'.format(dixi.config.get('addr'), args.channel), cookies=dixi.config.get('cookies'), data={'message': ' '.join(args.body)}).json()
    if 'error' in response:
        error(response['error'], args.color)
        sys.exit(6)
    success('Posted message to {}'.format(args.channel), args.color)
    print_message(response, len(response['author']), args.color)

def post_admin(args):
    if args.body == []:
        args.body = prompt_markdown('Message', args.color).split(' ')
        print(repr(args.body))
    response = requests.post('http://{}/admin/all'.format(dixi.config.get('addr')), cookies=dixi.config.get('cookies'), data={'message': ' '.join(args.body), 'server': 'true' if args.server else 'false'}).json()
    if 'error' in response:
        error(response['error'], args.color)
        sys.exit(6)
    success('Posted message to all channels'.format(args.channel), args.color)
    print_message(response, len(response['author']), args.color)



def main(args):
    if args.channel == 'users':
        users(args)
    elif args.channel == 'channels':
        channels(args)
    else:
        print(args)
        if args.body == [] and not args.post:
            view_post(args)
        elif args.all is True or args.server is True:
            post_admin(args)
        else:
            post(args)
