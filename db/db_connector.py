from mysql.connector import connect

from utils import get_db_conf


class BaseTable:
    sql_create: str = None
    sql_drop: str = None
    sql_insert: str = None
    sql_select_all: str = None
    sql_select_id: str = None
    sql_clear: str = None

    def __init__(self, connection):
        self.connection = connection

    def create(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql_create)
        self.connection.commit()

    def drop(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql_drop)
        self.connection.commit()

    def insert(self, param):
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql_insert, param)
        self.connection.commit()

    def insert_many(self, params):
        with self.connection.cursor() as cursor:
            cursor.executemany(self.sql_insert, params)
        self.connection.commit()

    def clear(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql_clear)
        self.connection.commit()

    def select_id(self, id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(self.sql_select_id, (id,))
            return cursor.fetchone()

    def select_many(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(self.sql_select_all)
            return cursor.fetchall()


class Users(BaseTable):
    sql_create = ('create table users '
                  '(id int,'
                  'sex int,'
                  'age int,'
                  'height int,'
                  'weight int,'
                  'activity int,'
                  'kcal float,'
                  'primary key (id))')
    sql_drop = 'drop table if exists users'
    sql_clear = 'delete from users'
    sql_insert = ('insert into users (id, sex, age, height, weight, activity, kcal)'
                  'values (%(id)s, %(sex)s, %(age)s, %(height)s, %(weight)s, %(activity)s, %(kcal)s)')
    sql_select_all = 'select * from users'
    sql_select_id = 'select * from users where id = %s'


class Products(BaseTable):
    sql_create = ('create table products '
                  '(id int auto_increment,'
                  'name varchar(100),'
                  'fat float,'
                  'protein float,'
                  'carbohydrates float,'
                  'kcal float,'
                  'primary key (id))')
    sql_drop = "drop table if exists products"
    sql_clear = 'delete from products'
    sql_insert = ("insert into products (name, fat, protein, carbohydrates, kcal) "
                  "values (%(name)s, %(fat)s, %(protein)s, %(carbohydrates)s, %(kcal)s)")
    sql_select_id = "select * from products where id = %s"
    sql_select_like = "select * from products where name like %(name)s limit %(limit)s"
    sql_select_name = "select id, name, kcal from products where name = %(name)s"
    sql_select_all = "select name, fat, protein, carbohydrates, kcal from products"

    def select_like(self, like, limit=30):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(self.sql_select_like, {'name': like + '%', 'limit': limit})
            return cursor.fetchall()

    def select_name(self, name):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(self.sql_select_name, {"name": name})
            return cursor.fetchall()


class UsersProducts(BaseTable):
    sql_create = ('create table users_products '
                  '(id int auto_increment,'
                  'user_id int,'
                  'product_id int,'
                  'time timestamp default current_timestamp,'
                  'mass float,'
                  'total_kcal float,'
                  'foreign key(user_id) references users(id) on delete cascade,'
                  'foreign key(product_id) references products(id) on delete set null,'
                  'primary key(id))')
    sql_drop = 'drop table if exists users_products'
    sql_clear = 'delete from users_products'
    sql_insert = 'insert into users_products (user_id, product_id, mass, total_kcal) values (%s, %s, %s, %s)'
    sql_select_today = ('SELECT users_products.total_kcal, users_products.time, products.name FROM users_products '
                        'INNER JOIN products ON users_products.product_id = products.id '
                        'where time > current_date() and user_id = %(user_id)s')

    sql_select_week = ("select user_id, SUM(total_kcal) as total_kcal, DATE(time) as time FROM users_products "
                       "WHERE time >= DATE_ADD(CURDATE(), INTERVAL -6 DAY) and user_id = %(user_id)s GROUP BY time")

    def select_today(self, user_id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(self.sql_select_today, {'user_id': user_id})
            return cursor.fetchall()

    def select_week(self, user_id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(self.sql_select_week, {'user_id': user_id})
            return cursor.fetchall()


class DBConnector:
    def __init__(self, **kwargs):
        self.connect_prop = kwargs
        self.connect_inst = None
        self.users: Users = None
        self.products: Products = None
        self.users_products: UsersProducts = None

    def recreate(self):
        self.users_products.drop()
        self.products.drop()
        self.users.drop()

        self.users.create()
        self.products.create()
        self.users_products.create()

    def connect(self):
        self.connect_inst = connect(**self.connect_prop)
        self.users = Users(self.connect_inst)
        self.products = Products(self.connect_inst)
        self.users_products = UsersProducts(self.connect_inst)

    def close(self):
        self.connect_inst.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    with DBConnector(**get_db_conf()) as db_connect:
        db_connect.recreate()
