import logging

from telegram.ext import Updater

from db import DBConnector
from handlers import add_handlers
from utils import get_bot_conf, get_db_conf

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    update = Updater(token=get_bot_conf().get('TOKEN'))

    add_handlers(update)

    with DBConnector(**get_db_conf()) as db_connect:
        update.dispatcher.bot_data['db_connect'] = db_connect
        update.start_polling()
        update.idle()
