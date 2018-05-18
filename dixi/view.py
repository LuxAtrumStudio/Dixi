import os
import sys
import json
import requests
import dixi.config
import dixi.markdown
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

def posts(color, update):
    if not update:
        content= requests.get("http://{}/".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
    else:
        content = requests.get("http://{}/".format(dixi.config.get('addr')), params={'update': update}, cookies=dixi.config.get('cookies')).json()
    posts = {}
    if 'error' in content:
        return {}, {}, None
    for key, value in content.items():
        if key != 'users' and key != 'update':
            posts[key] = value
    return posts, content['users'], content['update']

def post_message(color, message, channel):
    if message == str():
        return
    if channel is None:
        card = gen_card('Post', 1)
        error(card, 'must be logged in to post', color)
        timeout(dixi.config.get('timeout'))
        return
    render = dixi.markdown.render(message, 80, color)
    if dixi.config.get('post-prompt') == True:
        card = gen_card('Post', len(render.split('\n')) + 2)
        card.print(render)
        if action(card, 'Post message to {}'.format(channel), True, color):
            response = requests.post('http://{}/{}/post'.format(dixi.config.get('addr'), channel), cookies=dixi.config.get('cookies'), data={'message': message}).json()
            if 'error' in response:
                error(card, response['error'], color)
                timeout(dixi.config.get('timeout'))
                return False
            success(card, 'Posted message', color)
            timeout(dixi.config.get('timeout'))
            return True
        warning(card, 'Not Posting message', color)
        timeout(dixi.config.get('timeout'))
        return False
    else:
        response = requests.post('http://{}/{}/post'.format(dixi.config.get('addr'), channel), cookies=dixi.config.get('cookies'), data={'message': message}).json()
        if 'error' in response:
            return False
        else:
            return True



# def channels(args):
#     action('Getting Channel List', args.color)
#     content = requests.get("http://{}/channels/list".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
#     if 'error' in content:
#         error(content['error'], args.color)
#         sys.exit(3)
#     if len(content['channels']) == 0:
#         warning('no channels available to user', args.color)
#     else:
#         print_set([" * {}".format(x) for x in content['channels']])
#
# def users(args):
#     action('Getting User List', args.color)
#     content = requests.get("http://{}/users/list".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
#     current = content['current'] if 'current' in content else ''
#     data = []
#     for usr in sorted(content['users']):
#         if usr == current:
#             data.append('\033[1m * [{}]\033[0m'.format(print_user(usr, args.color)))
#         else:
#             data.append(' * {}'.format(print_user(usr, args.color)))
#     if (len(data) == 0):
#         warning('no users', args.color)
#     else:
#         print_set(data)
#
# def view_post(args):
#     response = dict()
#     if args.channel:
#         response = requests.get("http://{}/{}".format(dixi.config.get('addr'), args.channel), cookies=dixi.config.get('cookies')).json()
#         if 'error' in response:
#             error(response['error'], args.color)
#             sys.exit(5)
#         longest = max([len(x) for x in response['users']])
#         print_channel(args.channel, args.color)
#         for msg in response['messages']:
#             print_message(msg, longest, args.color)
#     else:
#         response = requests.get("http://{}/".format(dixi.config.get('addr')), cookies=dixi.config.get('cookies')).json()
#         if 'error' in response:
#             error(response['error'], args.color)
#             sys.exit(5)
#         if len(response) == 2:
#             warning('no posts on channels', args.color)
#             return
#         longest = max([len(x) for x in response['users']])
#         for channel in response:
#             if channel == 'users' or channel == 'update':
#                 continue
#             print_channel(channel, args.color)
#             for msg in response[channel]:
#                 print_message(msg, longest, args.color)
#             print()
#
# def post(args):
#     if args.body == []:
#         args.body = prompt_markdown('Message', args.color).split(' ')
#         print(repr(args.body))
#     response = requests.post('http://{}/{}/post'.format(dixi.config.get('addr'), args.channel), cookies=dixi.config.get('cookies'), data={'message': ' '.join(args.body)}).json()
#     if 'error' in response:
#         error(response['error'], args.color)
#         sys.exit(6)
#     success('Posted message to {}'.format(args.channel), args.color)
#     print_message(response, len(response['author']), args.color)
#
# def post_admin(args):
#     if args.body == []:
#         args.body = prompt_markdown('Message', args.color).split(' ')
#         print(repr(args.body))
#     response = requests.post('http://{}/admin/all'.format(dixi.config.get('addr')), cookies=dixi.config.get('cookies'), data={'message': ' '.join(args.body), 'server': 'true' if args.server else 'false'}).json()
#     if 'error' in response:
#         error(response['error'], args.color)
#         sys.exit(6)
#     success('Posted message to all channels'.format(args.channel), args.color)
#     print_message(response, len(response['author']), args.color)
#
