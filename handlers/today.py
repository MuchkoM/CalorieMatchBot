import datetime

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Updater

from db import DBConnector


def today(update: Update, context: CallbackContext):
    db_connect: DBConnector = context.bot_data['db_connect']
    result = db_connect.users_products.select_today(update.effective_user.id)
    user = db_connect.users.select_id(update.effective_user.id)
    reply_str = ''
    today_total = 0
    for i, row in enumerate(result):
        name = row['name']
        total_kcal = row['total_kcal']
        time: datetime.datetime = row['time']
        reply_str += f'{i + 1}. Product: {name}. Kcal: {total_kcal:.0f}. Time: {time.time()}\n'

        today_total += row['total_kcal']

    update.message.reply_text(reply_str and (f'{reply_str}'
                                             f'Today kcal eaten: {today_total:.0f} '
                                             f'Max allowed: {user["kcal"]:.0f}') or "Nothing was eaten today!")


def add_handler(updater: Updater):
    """/today - Eaten today"""
    updater.dispatcher.add_handler(CommandHandler('today', today))
