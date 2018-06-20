import sys
from dixi.output import display_length

class Pannel(object):

    def __init__(self, title=str(), dim=(0,0), pos=(0,0)):
        self.dim = dim
        self.pos = pos
        self.lines = []
        self.char_set = ('\u250C', '\u2500', '\u2510', '\u2502', '\u2502', '\u2514', '\u2500', '\u2518')
        self.bold_char_set = ('\u250F', '\u2501', '\u2513', '\u2503', '\u2503', '\u2517', '\u2501', '\u251B')
        self.char_set_title = ('\u2524', '\u251C')
        self.bold_char_set_title = ('\u252B', '\u2523')
        self.init = True
        self.title = title
        self.bold = False
        self.appendable = False
        self.cursor = -1
        self.scroll = 3

    def resize(self, dim):
        self.dim = dim

    def move(self, pos):
        self.pos = pos

    def clear(self, full=False):
        self.lines = []
        self.appendable = False
        if full:
            for i in range(1, self.dim[0] + 1):
                print(self.rel_pos(i,1), ' ' * (self.dim[1]), sep='')

    def pop(self):
        self.lines[-1] = ''

    def abs_pos(self, pos):
        return "\033[{};{}H".format(pos[0], pos[1])

    def rel_pos(self, a, b=None):
        if isinstance(a, tuple):
            a = list(a)
        if isinstance(a, list):
            if a[0] < 0:
                a[0] = self.dim[0] + a[0]
            if a[1] < 0:
                a[1] = self.dim[1] + a[1]
            return "\033[{};{}H".format(self.pos[0] + a[0], self.pos[1] + a[1])
        else:
            if a< 0:
                a = self.dim[0] + a
            if b < 0:
                b = self.dim[1] + b
            return "\033[{};{}H".format(self.pos[0] + a, self.pos[1] + b)

    def render_box(self):
        if self.bold:
            print(self.rel_pos((1, 1)), self.bold_char_set[0], self.bold_char_set[1] * (self.dim[1] - 2), self.bold_char_set[2], sep='')
            for i in range(2, self.dim[0]):
                print(self.rel_pos(i, 1), self.bold_char_set[3], self.rel_pos(i, self.dim[1]), self.bold_char_set[4], sep='')
            print(self.rel_pos((self.dim[0], 1)), self.bold_char_set[5], self.bold_char_set[6] * (self.dim[1] - 2), self.bold_char_set[7], sep='')
        else:
            print(self.rel_pos((1, 1)), self.char_set[0], self.char_set[1] * (self.dim[1] - 2), self.char_set[2], sep='')
            for i in range(2, self.dim[0]):
                print(self.rel_pos(i, 1), self.char_set[3], self.rel_pos(i, self.dim[1]), self.char_set[4], sep='')
            print(self.rel_pos((self.dim[0], 1)), self.char_set[5], self.char_set[6] * (self.dim[1] - 2), self.char_set[7], sep='')

    def render_title(self):
        if self.title:
            if self.bold:
                print(self.rel_pos(1, 2), self.bold_char_set_title[0], self.title, self.bold_char_set_title[1], sep='')
            else:
                print(self.rel_pos(1, 2), self.char_set_title[0], self.title, self.char_set_title[1], sep='')

    def print(self, *objects, sep=' ', end='\n', flush=True):
        string = sep.join([str(obj) for obj in objects]) + end
        if self.appendable:
            self.lines[-1] += string.split('\n')[0]
            self.lines += string.split('\n')[1:]
        else:
            self.lines += string.split('\n')
        if end != '\n':
            self.appendable = True
        else:
            self.appendable = False
        if flush:
            self.render()

    def move_to(self, pos):
        print(self.rel_pos(pos), end='')
        sys.stdout.flush()

    def toggle_bold(self):
        self.bold = not self.bold
        self.init = True

    def set_title(self, title):
        self.title = title
        self.init = True

    def toggle_cursor(self):
        if self.cursor == -1:
            self.cursor = 0
        else:
            self.cursor = -1
        self.init = True

    def cursor_set(self, pos=None):
        if pos:
            self.cursor = pos
        else:
            self.cursor = 0
    def cursor_up(self, dist=None):
        if dist:
            for i in range(dist):
                if self.cursor > 0:
                    self.cursor -= 1
        else:
            if self.cursor > 0:
                self.cursor -= 1

    def cursor_down(self, dist=None):
        display = self.get_display()
        if self.cursor == -1:
            return
        if dist:
            for i in range(dist):
                if self.cursor + self.dim[0] - self.scroll <= len(display):
                    self.cursor += 1
        else:
            if self.cursor + self.dim[0] - self.scroll <= len(display):
                self.cursor += 1

    def get_display(self):
        display_lines = []
        for line in self.lines:
            if display_length(line) > self.dim[1] - 2:
                tmp =str()
                length = 0
                for word in line.split(' '):
                    if length + display_length(word) + 1 >= self.dim[1] - 2:
                        length = 0
                        tmp = tmp[:-1] + '\n'
                    length += display_length(word) + 1
                    tmp += word + ' '
                line = tmp[:-1]
            if '\n' in line:
                display_lines += line.split('\n')
            elif line != '':
                display_lines.append(line)
        return display_lines

    def render(self):
        if self.init:
            self.render_box()
            self.render_title()
            self.init = False
        display_lines = self.get_display()
        if len(display_lines) < self.dim[0] - 2:
            for i, line in enumerate(display_lines):
                print(self.rel_pos(i+2, 2), line, sep='')
        else:
            if self.cursor == -1:
                count = len(display_lines)
                start = count - self.dim[0]
                for i in range(count - self.dim[0] + 2, count):
                    print(self.rel_pos(i-start, 2), display_lines[i], ' ' * (self.dim[1] - 2 - display_length(display_lines[i])), sep='')
            else:
                count = len(display_lines)
                start = self.cursor
                for i in range(self.cursor, min(count, start + self.dim[0] - 2)):
                    print(self.rel_pos(i-start+2, 2), display_lines[i], ' ' * ((self.dim[1] - 2) - display_length(display_lines[i])),sep='')

