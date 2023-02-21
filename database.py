import psycopg2

connection = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='1ngener_80RUS',
    database='postgres'
)

connection.autocommit = True


def create_table():
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id serial,
                first_name varchar(50) NOT NULL,
                last_name varchar(25) NOT NULL,
                vk_id varchar(50) NOT NULL PRIMARY KEY,
                vk_link varchar(50));"""
        )

def insert_data(first_name, last_name, vk_id, vk_link):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users (first_name, last_name, vk_id, vk_link) 
            VALUES ('{first_name}', '{last_name}', '{vk_id}', '{vk_link}');"""
        )

def search_id(vk_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT count(vk_id)
            FROM public.users
            WHERE vk_id='{vk_id}';"""
        )
        return cursor.fetchone()[0]

def drop_table():
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS users CASCADE;"""
        )
