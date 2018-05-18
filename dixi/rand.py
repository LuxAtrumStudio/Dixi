import math

STATE = 0xcafef00dd15ea5e5
MULTIPLIER = 6364136223846793005

def _init(val):
    global STATE
    STATE = 2 * val + 1
    rand()

def _rand():
    global STATE
    global MULTIPLIER
    x = STATE
    count = x >> 61
    STATE = x * MULTIPLIER
    x ^= x >> 22
    STATE = STATE % 18446744073709551615
    return (x >> (22 + count))

def seed(val):
    if isinstance(val, int):
        state = val
    elif isinstance(val, float):
        state = val
    elif isinstance(val, str):
        state = 0
        for ch in val:
            state = 131 * state + ord(ch)
    _init(state)

def rand(min_v=None, max_v=None):
    if min_v is None or max_v is None:
        return _rand()
    return _rand() % (max_v - min_v + 1) + min_v

def randf(min_v=0, max_v=1):
    return (_rand() % (int(max_v * 2147483647) - int(min_v * 2147483647)+ 1) + int(min_v * 2147483647)) / 2147483647
