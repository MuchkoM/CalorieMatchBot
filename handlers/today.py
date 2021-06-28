from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Updater

from db import DBConnector


def today(update: Update, context: CallbackContext):
    db_connect: DBConnector = context.bot_data['db_connect']
    result = db_connect.users_products.select_today(update.effective_user.id)
    reply_str = ''
    for row in result:
        reply_str += '{}\n'.format(row)

    update.message.reply_text(reply_str or "Nothing was eaten today!")


def add_handler(updater: Updater):
    updater.dispatcher.add_handler(CommandHandler('today', today))
