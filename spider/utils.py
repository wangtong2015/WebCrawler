import sys

def log_progress(index, length, msg=''):
    if(index == 0):
        print()
    sys.stdout.write("\r{0:>10.2f}%{1:>20}".format(index / length * 100, msg))
    sys.stdout.flush()
