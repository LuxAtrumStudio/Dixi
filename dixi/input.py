import signal

class Timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.setitimer(signal.ITIMER_REAL, self.seconds)
    def __exit__(self, type, value, traceback):
        signal.setitimer(signal.ITIMER_REAL, 0)

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self):
        return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

def timeout(sec):
    if sec is None:
        sec = 1
    try:
        with Timeout(sec):
            return getch()
    except:
        pass
    return None

def getinput(sec = None):
    if sec is not None:
        try:
            with Timeout(sec):
                return getinput()
        except:
            pass
        return None
    key = getch()
    if ord(key) == 27:
        ch = timeout(0.05)
        if not ch:
            return 'ESCAPE'
        if ord(ch) == 91:
            ch = timeout(0.05)
            if ord(ch) == 49:
                ch = timeout(0.05)
                if ord(ch) == 59:
                    ch = timeout(0.05)
                    if ord(ch) == 53:
                        ch = timeout(0.05)
                        if ord(ch) == 65:
                            return 'CTRL_UP'
                        elif ord(ch) == 66:
                            return 'CTRL_DOWN'
                        elif ord(ch) == 67:
                            return 'CTRL_RIGHT'
                        elif ord(ch) == 68:
                            return 'CTRL_LEFT'
            elif ord(ch) == 51:
                ch = timeout(0.05)
                if ord(ch) == 126:
                    return 'DELETE'
            elif ord(ch) == 65:
                return 'UP'
            elif ord(ch) == 66:
                return 'DOWN'
            elif ord(ch) == 67:
                return 'RIGHT'
            elif ord(ch) == 68:
                return 'LEFT'
    elif ord(key) == 9:
        return 'TAB'
    elif ord(key) == 13:
        return 'ENTER'
    elif ord(key) == 127:
        return 'BACKSPACE'
    else:
        return key
