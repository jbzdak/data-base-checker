__author__ = 'jb'


import os


def read_file(current_file, file_name):
    with open(os.path.join(os.path.split(current_file)[0], file_name)) as f:
        return f.read()

