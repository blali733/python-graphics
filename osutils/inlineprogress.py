import sys


def inline_percent_progress(percent_value):
    print(percent_value.__str__()+"% completed                  ", end='\r')
    sys.stdout.flush()


def inline_out_of_progress(value, out_of, what=''):
    print(value.__str__()+"/"+out_of.__str__()+" "+what+" completed                  ", end='\r')
    sys.stdout.flush()


def inline_out_of_progress_long(value, out_of, what=''):
    print(value.__str__()+" out of "+out_of.__str__()+" "+what+" completed                  ", end='\r')
    sys.stdout.flush()
