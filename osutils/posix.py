import sys
import tty
import termios


def start_key_listener():
    """
    Switches console to allow servicing of keyboard in raw mode.

    Returns
    -------
    Backup of console parameters.
    """
    params = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    return params


def get_key_value():
    """
    Returns pressed key.

    Returns
    -------
    string
        Single character read from keyboard
    """
    return sys.stdin.read(1)[0]


def stop_key_listener(params):
    """
    Switches console back to state passed as parameter.

    Parameters
    ----------
    params
        Console parameters (preferably obtained by previous call of start_key_listener())
    """
    termios.tcsetattr(sys.stdin, termios.TCSANOW, params)
