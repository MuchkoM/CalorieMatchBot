from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters, Updater

from db import DBConnector
from utils import send_like_product

EAT_1, EAT_2 = range(2)


def eat_0(update: Update, _: CallbackContext):
    update.message.reply_text('What do you want to eat?')
    return EAT_1


def eat_1(update: Update, context: CallbackContext):
    db_connect: DBConnector = context.bot_data['db_connect']
    result = db_connect.products.select_name(update.message.text)

    if len(result) == 1:
        update.message.reply_text('How match do you want to eat?')
        context.user_data['product'] = result[0]
        return EAT_2
    else:
        send_like_product(update, context, update.message.text)
        update.message.reply_text('What do you want to eat?')
        return EAT_1


def eat_2(update: Update, context: CallbackContext):
    db_connect: DBConnector = context.bot_data['db_connect']

    product = context.user_data['product']
    del context.user_data['product']

    mass = float(update.message.text)

    db_connect.users_products.insert(
        (update.effective_user.id,
         product['id'],
         mass,
         mass * product['kcal'] / 100)
    )
    update.message.reply_text('{name} was eaten'.format(**product))
    return ConversationHandler.END


def add_handler(updater: Updater):
    """/eat - Eat product"""
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('eat', eat_0)],
        states={
            EAT_1: [MessageHandler(Filters.text & ~Filters.command, eat_1)],
            EAT_2: [MessageHandler(Filters.text & ~Filters.command, eat_2)],
        },
        fallbacks=[],
    ))
