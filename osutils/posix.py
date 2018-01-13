import sys
import tty


def start_key_listener():
    tty.setraw(sys.stdin)


def get_key_value():
    return sys.stdin.read(1)[0]


def stop_key_listener():
    tty.setcbreak(sys.stdin)
