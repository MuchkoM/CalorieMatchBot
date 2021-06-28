from telegram import Update
from telegram.ext import Updater, CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters

from db import DBConnector
from utils import cancel

import re

str_matcher = r"\"(?P<name>.+)\"\s*(?P<fat>\d+)\s*/\s*(?P<protein>\d+)\s*/\s*(?P<carbohydrates>\d+)\s*(?P<kcal>\d+)"

ADD_1 = 0


def add_0(update: Update, _: CallbackContext):
    update.message.reply_text('Enter new product in format\n'
                              '"name" fat/protein/carbohydrates kcal')
    return ADD_1


def add_1(update: Update, context: CallbackContext):
    db_connect: DBConnector = context.bot_data['db_connect']
    result = re.match(str_matcher, update.message.text)
    if result:
        db_connect.products.insert(result.groupdict())
        update.message.reply_text('Product was added')
    else:
        update.message.reply_text('Message have wrong format')
    return ConversationHandler.END


def add_handler(updater: Updater):
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('product_add', add_0)],
        states={
            ADD_1: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, add_1)]
        },
        fallbacks=[]
    ))
