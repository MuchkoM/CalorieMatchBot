import re

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters, Updater

from db import DBConnector
from utils import kcal_calc

START_0 = 0

match_str = r'(?P<age>\d+)/(?P<sex>(male)|(female))/(?P<height>\d+)/(?P<weight>\d+)/(?P<activity>[0-5])'


def start_0(update: Update, context: CallbackContext):
    db_connect: DBConnector = context.bot_data['db_connect']
    update.message.reply_text('Hello I`m bot')
    db_user = db_connect.users.select_id(update.effective_user.id)
    if db_user:
        update.message.reply_text('Welcome back!\n'
                                  'Your eat kcal per day: {kcal}'.format(**db_user))
        return ConversationHandler.END
    else:
        update.message.reply_text("Hello new user!\n"
                                  "Enter your physical parameters:\n"
                                  "age/sex('male' or 'female')/height/weight/activity(0-5)")

        return START_0


def start_1(update: Update, context: CallbackContext):
    db_connect: DBConnector = context.bot_data['db_connect']
    res = re.match(match_str, update.message.text)
    if res:
        user = {
            'id': update.effective_user.id,
            'age': int(res['age']),
            'weight': int(res['weight']),
            'height': int(res['height']),
            'sex': 0 if res['sex'] == 'male' else 1,
            'activity': int(res['activity'])
        }

        user['kcal'] = kcal_calc(**user)
        db_connect.users.insert(user)

        update.message.reply_text('Success')
        return ConversationHandler.END
    else:
        update.message.reply_text('Wrong format\n'
                                  'Reply again')
        return START_0


def add_handler(updater: Updater):
    """/start - Start bot"""
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start_0)],
        states={
            START_0: [MessageHandler(Filters.text & ~Filters.command, start_1)]
        },
        fallbacks=[],
    ))
