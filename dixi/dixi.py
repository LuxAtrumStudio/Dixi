import argparse
import os
import sys

import dixi.config
import dixi.user
import dixi.channel
import dixi.view
from dixi.output import error

def set_default_subparser(self, name, args=None):
    """default subparser selection. Call after setup, just before parse_args()
    name: is the name of the subparser to call by default
    args: if set is the argument list handed to parse_args()

    , tested with 2.7, 3.2, 3.3, 3.4
    it works with 2.6 assuming argparse is installed
    """
    subparser_found = False
    existing_default = False
    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
                if sp_name == name:
                    existing_default = True
        if not subparser_found:
            if not existing_default:
                for x in self._subparsers._actions:
                    if not isinstance(x, argparse._SubParsersAction):
                        continue
                    x.add_parser(name)
                    break
            if args is None:
                sys.argv.insert(1, name)
            else:
                args.insert(0, name)

def main():
    argparse.ArgumentParser.set_default_subparser = set_default_subparser
    parser = argparse.ArgumentParser(description="Dixi-CLI")
    subparser = parser.add_subparsers( help='Different actions to preform', dest='command')

    # >>>>>>>>>> VIEW <<<<<<<<< #
    view = subparser.add_parser('view', help='View recent posts')
    view.add_argument('channel', nargs='?', help='Channel to view posts from')
    view.add_argument('-p', '--post', action='store_true', help='Enables post prompt')
    view.add_argument('-a', '--all', action='store_true', help='Sends post to all channels')
    view.add_argument('-s', '--server', action='store_true', help='Sends post as server')
    view.add_argument('--no-color', action='store_false', dest='color', help='Disable color in output')
    view.add_argument('body', nargs='*', help='String to post')

    # >>>>>>>>>> USER <<<<<<<<< #
    user = subparser.add_parser('user', help='Manage user profile')
    user_subparser = user.add_subparsers(help='Different user based actions to preform', dest='user_command')

    # >>>>> REGISTER <<<<< #
    register = user_subparser.add_parser('register', help='Register new user account')
    register.add_argument('name', nargs='?', help='Username')
    register.add_argument('email', nargs='?', help='Recovery email address')
    register.add_argument('password', nargs='?', help='Password')
    register.add_argument('password2', nargs='?', help='Password Confirmation')
    register.add_argument('--no-color', action='store_false', dest='color', help='Disable color in output')

    # >>>>> LOGIN <<<<< #
    login = user_subparser.add_parser('login', help='Login to user account')
    login.add_argument('name', nargs='?', help='Username')
    login.add_argument('password', nargs='?', help='Password')
    login.add_argument('--no-color', action='store_false', dest='color', help='Disable color in output')

    # >>>>> LOGOUT <<<<< #
    logout = user_subparser.add_parser('logout', help='Logout from user account')
    logout.add_argument('--no-color', action='store_false', dest='color', help='Disable color in output')

    # >>>>> DELETE <<<<< #
    user_delete = user_subparser.add_parser('delete', help='Delete user account')
    user_delete.add_argument('name', nargs='?', help='User account to delete[Current]')
    user_delete.add_argument('--no-color', action='store_false', dest='color', help='Disable color in output')

    # >>>>>>>>>> CHANNEL <<<<<<<<<< #
    channel = subparser.add_parser('channel', help='Manage channels')
    channel_subparser = channel.add_subparsers(help='Different channel based actions to preform', dest='channel_command')

    # >>>>> CREATE <<<<< #
    create = channel_subparser.add_parser('create', help='Create a new channel')
    create.add_argument('title', nargs='?', help='Channel title')
    create.add_argument('users', nargs='*', help='Users who will have access to the channel')
    create.add_argument('--no-color', action='store_false', dest='color', help='Disable color in output')

    # >>>>> DELETE <<<<< #
    channel_delete = channel_subparser.add_parser('delete', help='Delete channel')
    channel_delete.add_argument('channel', nargs='?', help='Channel to delete')
    channel_delete.add_argument('--no-color', action='store_false', dest='color', help='Disable color in output')

    # >>>>>>>>>> CONFIG <<<<<<<<<< #
    config = subparser.add_parser('config', help='Manage configuration')
    config.add_argument('--addr', help='Default host address')
    config.add_argument('--no-color', action='store_false', dest='color', help='Disable color in output')

    parser.set_default_subparser('view')
    args = parser.parse_args()
    if args.command != 'config' and not dixi.config.exists('addr'):
        error('Must set host address before accessing server', args.color)
        sys.exit(7)
    if args.command == 'user':
        dixi.user.main(args)
    elif args.command == 'channel':
        dixi.channel.main(args)
    elif args.command == 'view':
        dixi.view.main(args)
    elif args.command == 'config':
        dixi.config.main(args)
