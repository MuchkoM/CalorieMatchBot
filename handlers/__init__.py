from telegram.ext import Updater
from importlib import import_module

import os


def add_handlers(updater: Updater):
    directory = os.path.dirname(__file__)
    for file in os.listdir(directory):
        base, ext = os.path.splitext(file)
        if ext == ".py" and base != '__init__' and os.path.isfile(os.path.join(directory, file)):
            module = import_module('.' + base, __name__)
            add_handler = getattr(module, 'add_handler', None)

            if add_handler:

                if hasattr(add_handler, '__call__'):
                    add_handler(updater)
                else:
                    print("add_handler is not callable")

            else:
                print("module {} don't have add_handler property".format(module.__name__))
