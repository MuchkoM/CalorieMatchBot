import logging

from telegram.ext import Updater

from db import DBConnector
from handlers import add_handlers
from utils import get_bot_conf, get_db_conf

if __name__ == '__main__':
    bot_conf = get_bot_conf()
    logging.basicConfig(level=bot_conf.get('LEVEL'))
    update = Updater(token=bot_conf.get('TOKEN'))

    add_handlers(update)

    with DBConnector(**get_db_conf()) as db_connect:
        update.dispatcher.bot_data['db_connect'] = db_connect
        update.start_polling()
        update.idle()
