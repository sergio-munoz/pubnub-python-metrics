import os
import inspect
import json

def get_func_name():
    frame = inspect.currentframe()
    return inspect.getframeinfo(frame).function

def get_os_dir():
    return str(os.path.dirname(os.path.abspath(__file__)))

def get_file_dir():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))