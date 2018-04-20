import sys


def inline_percent_progress(percent_value):
    """
    Method intended to show percentage of progress in updated text line.

    Parameters
    ----------
    percent_value : float
        Percentage of progress.
    """
    # UNTESTABLE
    print(percent_value.__str__()+"% completed                  ", end='\r')
    sys.stdout.flush()


def inline_out_of_progress(value, out_of, what=''):
    """
    Method intended to show progress as (a/b) in updated text line.

    Parameters
    ----------
    value : int
        Current value
    out_of : int
        Maximal value
    what : string
        Additional description
    """
    # UNTESTABLE
    print(value.__str__()+"/"+out_of.__str__()+" "+what+" completed                  ", end='\r')
    sys.stdout.flush()


def inline_out_of_progress_long(value, out_of, what=''):
    """
    Method intended to show progress as (a out of b) in updated text line.

    Parameters
    ----------
    value : int
        Current value
    out_of : int
        Maximal value
    what : string
        Additional description
    """
    # UNTESTABLE
    print(value.__str__()+" out of "+out_of.__str__()+" "+what+" completed                  ", end='\r')
    sys.stdout.flush()
