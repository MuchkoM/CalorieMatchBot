import os
from importlib import import_module

from telegram import Update
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackContext


def add_handlers(updater: Updater, additional_help_str=''):
    directory = os.path.dirname(__file__)
    help_str_list = ['/help - Show current help']
    for file in os.listdir(directory):
        base, ext = os.path.splitext(file)
        if ext == ".py" and base != '__init__' and os.path.isfile(os.path.join(directory, file)):
            module = import_module('.' + base, __name__)
            add_handler = getattr(module, 'add_handler', None)

            if add_handler:

                if hasattr(add_handler, '__call__'):
                    add_handler(updater)
                    help_str_list.append(add_handler.__doc__)
                else:
                    print("add_handler is not callable")

            else:
                print("module {} don't have add_handler property".format(module.__name__))

    help_str_list.append(additional_help_str)

    def help_cmd(update: Update, _: CallbackContext):
        update.message.reply_text('\n'.join(help_str_list))

        return ConversationHandler.END

    updater.dispatcher.add_handler(CommandHandler('help', help_cmd))
