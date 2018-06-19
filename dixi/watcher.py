#!/usr/bin/python3

from json import loads
from sys import argv, exit
from time import sleep
from datetime import datetime
from subprocess import Popen
from requests import get

def main(color, addr, cookies, channel, age, delay):
    mili_delay = 3 * (delay * 1000)
    update = int(datetime.now().timestamp() * 1000) - mili_delay
    age = (age * 1000) + update
    if channel:
        url = "http://{}/{}/".format(addr, channel)
    else:
        url = "http://{}/".format(addr)
    while True:
        sleep(delay)
        if update > age:
            exit(0)
        try:
            response = get("{}?update={}".format(url, update), cookies=cookies).json()
        except:
            Popen(['notify-send', 'HTTP error'])
            exit(0)
        update = response['update'] - mili_delay
        print(response)
        channels = []
        for key, value in response.items():
            if key in ('users', 'update'):
                continue
            if value:
                channels.append([key, len(value)])
        msg = '\n'.join(list(map(lambda x: "{}: {}".format(x[0], x[1]), channels)))
        if msg:
            Popen(['notify-send', "Dixi", msg])

if __name__ == "__main__":
    main(True if argv[1] == 'True' else False, argv[2], loads(argv[3]), argv[4], int(argv[5]), int(argv[6]))

