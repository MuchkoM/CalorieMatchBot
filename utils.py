import os

from dotenv import dotenv_values
from telegram import Update
from telegram.ext import CallbackContext


def chunks(itr, mapper, max_n=64):
    """Yield successive n-sized chunks from lst."""
    res = []
    i = 0
    for row in itr:
        if i % max_n == 0 and res:
            yield res
            res = []
        res.append(mapper(row))

        i += 1

    yield res


def kcal_calc(weight, height, age, sex, activity, **kwargs):
    if sex == 0:
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

    if activity == 0:
        bmr *= 1.2
    elif activity == 1:
        bmr *= 1.375
    elif activity == 2:
        bmr *= 1.55
    elif activity == 3:
        bmr *= 1.725
    elif activity == 4:
        bmr *= 1.9

    return bmr


def send_like_product(update: Update, context: CallbackContext, name: str):
    db_connect = context.bot_data['db_connect']
    result = db_connect.products.select_like(name, 20)

    if result:
        res_str = 'Likes products\n'
        res_str += 'Product: F\\P\\C Kcal\n'
        for row in result:
            res_str += '"{name}": {fat}\\{protein}\\{carbohydrates} {kcal}\n'.format(**row)
        update.message.reply_text(res_str)
    else:
        update.message.reply_text('Not found')


def get_db_conf():
    return dotenv_values(os.path.join(os.path.dirname(__file__), '.env.db'))


def get_bot_conf():
    return dotenv_values(os.path.join(os.path.dirname(__file__), '.env.bot'))
