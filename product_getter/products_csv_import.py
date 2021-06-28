import logging

import pandas

from db import DBConnector
from utils import chunks, get_db_conf

logging.basicConfig(level=logging.DEBUG)

with DBConnector(**get_db_conf()) as db_connect:
    db_connect.products.clear()
    print(len(db_connect.products.select_many()))

    df = pandas.read_csv('products.csv', sep=',', encoding='utf8')

    for chunk in chunks(df.itertuples(), lambda x: x._asdict(), 256):
        db_connect.products.insert_many(chunk)

    print(len(db_connect.products.select_many()))
