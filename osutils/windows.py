import msvcrt


def start_key_listener():
    """
    UNUSED - compatibility with POSIX equivalent.

    Returns
    -------
    int
        0 value.
    """
    return 0


def get_key_value():
    """
    Returns pressed key.

    Returns
    -------
    string
        Single character read from keyboard
    """
    return msvcrt.getwch()


def stop_key_listener(params):
    """
    UNUSED - compatibility with POSIX equivalent.

    Parameters
    ----------
    params : anything
        UNUSED - compatibility with POSIX equivalent.
    """
    pass
