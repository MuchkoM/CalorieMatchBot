from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackContext, Updater

from utils import send_like_product

PRODUCT_LIKE_1 = 0


def like_product_0(update: Update, _: CallbackContext):
    update.message.reply_text('Enter start part of product name:')

    return PRODUCT_LIKE_1


def like_product_1(update: Update, context: CallbackContext):
    send_like_product(update, context, update.message.text)
    return ConversationHandler.END


def add_handler(updater: Updater):
    """/products_similar - List similar products"""
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('products_similar', like_product_0)],
        states={
            PRODUCT_LIKE_1: [MessageHandler(Filters.text & ~Filters.command, like_product_1)]
        },
        fallbacks=[],
    ))
