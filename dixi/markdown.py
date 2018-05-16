import os
import re

from dixi.color import get_color

def render(markdown, width=80, color=True):
    header_underline = ('\u2501', '\u2500', '', '', '')
    response = str()
    block = None
    stack = []
    headers = []
    blocks = {'code': [7, '\u2502 ', '```'], 'math': [4, '\u2502 ', '$$']}
    inlines = [['emph', '\033[1m', '\033[21m', re.compile('\*\*'), re.compile('__')], ['ital', '\033[3m', '\033[23m', re.compile('\*'), re.compile('_')], ['strk', '\033[9m', '\033[29m', re.compile('--')], ['math', get_color(4, False, color), get_color('default', False, color), re.compile('\$')], ['code', get_color(9, False, color) + get_color(0, True, color), get_color('default', False, color) + get_color('default', True, color), re.compile('`')]]
    for i in range(1, 6):
        headers.append(re.compile('^{0} ([^#]+) {0}$'.format('#' * i)))
    for line in markdown.split('\n'):
        state = None
        if block:
            if line == blocks[block][2]:
                block = None
                continue
            line = get_color(blocks[block][0], False, color) + blocks[block][1] + line + '\n' + get_color('default', False, color)
            state = block
        if not state:
            for i, head in enumerate(headers):
                match = head.match(line)
                if match:
                    state = 'header'
                    line = get_color(14 - i, False, color) + "\033[1m" + match.groups()[0] + '\033[0m\n'
        if not state and line.strip() in ('***', '---'):
            if line.strip() == '***':
                line = get_color(7, False, color)
            else:
                line = get_color(6, False, color)
            line += '\u2500' * width + '\n' + get_color('default', False, color)
            state = 'sep'
        if not state and line.startswith('> '):
            state = 'quote'
            line = get_color(8, False, color) + '\u2503' + line[1:] + get_color('default', False, color) +'\n'
        elif line.startswith('```'):
            state = 'code'
            block = 'code'
            continue
        elif line.startswith('$$'):
            state = 'math'
            block = 'math'
            continue
        if not state and line.strip().startswith('* '):
            state = 'list'
            space = len(line) - len(line.lstrip())
            line = line.lstrip().lstrip('* ')
            line = (' ' * space) + '\u2022 ' + line + '\n'
        for inline in inlines:
            matched = True
            while matched:
                matched = False
                for reg in inline[3:]:
                    tmp = line[:]
                    if stack and stack[-1] == inline[0]:
                        line = reg.sub(inline[2], line, 1)
                        if line != tmp:
                            matched = True
                            stack.pop()
                    else:
                        line = reg.sub(inline[1], line, 1)
                        if line != tmp:
                            matched = True
                            stack.append(inline[0])

        if not state:
            line += '\n'
        response += line
    # response += "\033[0m"
    return response[:-1] + "\033[0m"
