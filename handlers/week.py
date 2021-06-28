from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from db import DBConnector


def week(update: Update, context: CallbackContext):
    db_connect: DBConnector = context.bot_data['db_connect']
    result = db_connect.users_products.select_week(update.effective_user.id)
    res_str = ''
    for day in result:
        res_str += '{time}: {total_kcal:.0f} kcal\n'.format(**day)
    update.message.reply_html(res_str or 'Nothing was eaten this week!')


def add_handler(updater: Updater):
    """/week - Get week overview"""
    updater.dispatcher.add_handler(CommandHandler('week', week))
