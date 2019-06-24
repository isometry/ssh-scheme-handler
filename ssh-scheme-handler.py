#!/usr/bin/env python3
"""
SSH Scheme Handler for FreeDesktop/XDG
(c) Robin Breathe, 2019
"""
import sys
import os
from argparse import ArgumentParser
from urllib.parse import urlparse


TERMINAL_SEARCH_ORDER = [
    'xfce4-terminal',
    'gnome-terminal',
    'urxvt',
    'xterm'
]
TERMINAL_SPECS = {
    'gnome-terminal': {
        'executable': 'gnome-terminal',
        'extra_args': ['--quiet', '--tab', '--active'],
        'flags': {
            'title': '--title',
            'execute': '--'
        }
    },
    'kitty': {
        'executable': 'kitty',
        'extra_args': ['@', 'new-window', '--new-tab'],
        'flags': {
            'title': '--tab-title',
            'execute': '--'
        }
    },
    'tmux': {
        'executable': 'tmux',
        'extra_args': ['new-window'],
        'flags': {
            'title': '-n',
            'execute': None
        }
    },
    'urxvt': {
        'executable': 'urxvt',
        'flags': {
            'title': '-title',
            'execute': '-e'
        }
    },
    'xfce4-terminal': {
        'executable': 'xfce4-terminal',
        'extra_args': ['--tab', '--hold'],
        'flags': {
            'title': '--title',
            'execute': '--execute'
        }
    },
    'xterm': {
        'executable': 'xterm',
        'flags': {
            'title': '-title',
            'execute': '-e'
        }
    }
}
SCHEMES = {
    'ssh': {
        'executable': 'ssh',
        'port_flag': '-p'
    },
    'mosh': {
        'executable': 'mosh',
        'port_flag': '-p'
    }
}


def best_available_terminal(terminals=TERMINAL_SEARCH_ORDER):
    from shutil import which
    return next(x for x in terminals if which(x))


def main():
    parser = ArgumentParser(
        description="SSH Scheme Handler for XFCE4 Terminal")
    parser.add_argument('-d', '--debug', action='store_true',
                        help='debug')
    parser.add_argument('--direct', action='store_true',
                        help='bypass terminal emulator')
    parser.add_argument('-t', '--terminal', action='store',
                        choices=TERMINAL_SPECS.keys(),
                        help='set preferred terminal emulator')
    parser.add_argument('url', metavar='ssh://[user@]host[:port]', action='store',
                        help='extended SSH scheme')
    args = parser.parse_args()

    url = urlparse(args.url)

    if url.scheme not in SCHEMES:
        parser.error("error: unsupported scheme '{}'".format(url.scheme))

    if url.hostname is None:
        parser.error("error: no host specified")

    if url.path not in ('', '/'):
        parser.error("error: scheme path is not supported")

    scheme = SCHEMES[url.scheme]

    if args.direct:
        cmd_path = scheme['executable']
        cmd_args = [cmd_path]
    else:
        terminal = TERMINAL_SPECS[args.terminal
                                  or os.getenv('PREFERRED_TERMINAL_EMULATOR')
                                  or best_available_terminal()]
        cmd_path = terminal['executable']
        cmd_args = [cmd_path]
        cmd_args += terminal.get('extra_args', [])
        if terminal['flags'].get('title') is not None:
            cmd_args += [terminal['flags']['title'],
                         '@'.join((url.username or '', url.hostname))]
        if terminal['flags'].get('execute') is not None:
            cmd_args += [terminal['flags']['execute']]
        cmd_args += [scheme['executable']]

    if url.port is not None:
        cmd_args += [scheme['port_flag'], str(url.port)]

    if url.username is None:
        cmd_args += [url.hostname]
    else:
        cmd_args += ['@'.join((url.username, url.hostname))]

    if args.debug:
        print('execvp({})'.format(cmd_args), file=sys.stderr)
    else:
        os.execvp(cmd_path, cmd_args)


if __name__ == '__main__':
    main()
