import sys
import tty
import termios


def start_key_listener():
    params = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    return params


def get_key_value():
    return sys.stdin.read(1)[0]


def stop_key_listener(params):
    termios.tcsetattr(sys.stdin, termios.TCSANOW, params)
