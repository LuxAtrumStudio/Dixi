import os
import re

from dixi.color import get_color, get_color_ability, Access


def code(block, color=True):
    if color is False or block[1] == str():
        return block[0], False
    try:
        from pygments import highlight
        from pygments.lexers import (get_lexer_by_name, get_lexer_for_filename,
                                     get_lexer_for_mimetype)
        from pygments.formatters import TerminalTrueColorFormatter, Terminal256Formatter, TerminalFormatter
        try:
            lexer = get_lexer_by_name(block[1])
        except:
            return block[0], False
        ab = get_color_ability()
        if ab == Access.COLOR_TRUE:
            formatter = TerminalTrueColorFormatter()
        elif ab == Access.COLOR_256:
            formatter = Terminal256Formatter()
        elif ab == Access.COLOR_8 or ab == Access.COLOR_16:
            formatter = TerminalFormatter()
        else:
            formatter = None
        if formatter is None:
            return block[0], False
        result = highlight(block[0], lexer, formatter)
        return result, True
    except ImportError:
        return block[0], False


def render(markdown, width=80, color=True):
    header_underline = ('\u2501', '\u2500', '', '', '')
    response = str()
    block = None
    stack = []
    headers = []
    blocks = {'code': [7, '\u2502 ', '```'], 'math': [4, '\u2502 ', '$$']}
    inlines = [[
        'emph', '\033[1m', '\033[21m',
        re.compile('\*\*'),
        re.compile('__')
    ], [
        'ital', '\033[3m', '\033[23m',
        re.compile('\*'),
        re.compile('_')
    ], [
        'strk', '\033[9m', '\033[29m',
        re.compile('--')
    ], [
        'math',
        get_color(4, False, color),
        get_color('default', False, color),
        re.compile('\$')
    ], [
        'code',
        get_color(9, False, color) + get_color(0, True, color),
        get_color('default', False, color) + get_color('default', True, color),
        re.compile('`')
    ]]
    for i in range(1, 6):
        headers.append(re.compile('^{0} ([^#]+) {0}$'.format('#' * i)))
    block_data = [None, None]
    for line in markdown.split('\n'):
        state = None
        if block:
            if line == blocks[block][2]:
                res = False
                if block == 'code':
                    block_data[0], res = code(block_data, color)
                # line = line[:-1]
                if res:
                    line = get_color(blocks[block][0], False,
                                     color) + blocks[block][1] + get_color(
                                         'default', False,
                                         color) + block_data[0][:-1]
                    line = line.replace(
                        '\n',
                        '\n' + get_color(blocks[block][0], False, color) +
                        blocks[block][1] + get_color('default', False, color))
                else:
                    line = get_color(
                        blocks[block][0], False,
                        color) + blocks[block][1] + block_data[0][:-1]
                    line = line.replace(
                        '\n',
                        get_color('default', False, color) + '\n' + get_color(
                            blocks[block][0], False, color) + blocks[block][1])
                    line = line + get_color('default', False, color)
                line += '\n'
                response += line
                block_data = [None, None]
                block = None
                continue
            block_data[0] += line + '\n'
            line = str()
            # line = get_color(blocks[block][0], False,
            #                  color) + blocks[block][1] + line + get_color(
            #                      'default', False, color) + '\n'
            state = block
        if not state:
            for i, head in enumerate(headers):
                match = head.match(line)
                if match:
                    state = 'header'
                    line = get_color(
                        14 - i, False,
                        color) + "\033[1m" + match.groups()[0] + '\033[0m\n'
        if not state and line.strip() in ('***', '---'):
            if line.strip() == '***':
                line = get_color(7, False, color)
            else:
                line = get_color(6, False, color)
            line += '\u2500' * width + get_color('default', False,
                                                 color) + '\n'
            state = 'sep'
        if not state and line.startswith('> '):
            state = 'quote'
            line = get_color(8, False,
                             color) + '\u2503' + line[1:] + get_color(
                                 'default', False, color) + '\n'
        elif line.startswith('```'):
            state = 'code'
            block = 'code'
            block_data = [str(), line[3:].strip()]
            continue
        elif line.startswith('$$'):
            state = 'math'
            block = 'math'
            block_data = [str(), None]
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
            if len(line) >= width:
                length = 0
                cp = line[:]
                line = ''
                for ch in cp.split(' '):
                    if length + len(ch) + 1 >= width:
                        line += '\n' + ch
                        length = 0
                    else:
                        line += ' ' + ch
                    length += len(ch) + 1
                line = line[1:]
            line += '\n'
        response += line
    if block_data[0] is not None:
        res = False
        if block == 'code':
            tmp, res = code(block_data, color)
        if res:
            line = get_color(blocks[block][0], False,
                             color) + blocks[block][1] + get_color(
                                 'default', False,
                                 color) + tmp[:-1]
            line = line.replace(
                '\n',
                '\n' + get_color(blocks[block][0], False, color) +
                blocks[block][1] + get_color('default', False, color))
        else:
            line = get_color(
                blocks[block][0], False,
                color) + blocks[block][1] + block_data[0][:-1]
            line = line.replace(
                '\n',
                get_color('default', False, color) + '\n' + get_color(
                    blocks[block][0], False, color) + blocks[block][1])
            line = line + get_color('default', False, color)
        response += line + '\n'
    return response[:-1] + "\033[0m"
