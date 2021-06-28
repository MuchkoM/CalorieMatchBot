from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from db import DBConnector
from utils import chunks


def print_products(update: Update, context: CallbackContext):
    db_connect: DBConnector = context.bot_data['db_connect']
    products = db_connect.products.select_many()
    for chunk in chunks(products, lambda x: x, 64):
        res_str = ''
        for row in chunk:
            res_str += '"{name}" {fat}/{protein}/{carbohydrates} {kcal}\n'.format(**row)
        update.message.reply_text(res_str)


def add_handler(updater: Updater):
    """/products - List of all product"""
    updater.dispatcher.add_handler(CommandHandler('products', print_products))
