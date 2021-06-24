import os
from dotenv import load_dotenv
import psycopg2

load_dotenv("./.env.local")

con = cur = db = None

if 'DATABASE_URI' in os.environ:
    DATABASE_URL = os.environ['DATABASE_URI']
else:
    raise ValueError('Env Var not found!')

# TODO: Error ka kuch to karo


def connect():
    global con, cur, db
    try:
        con = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = con.cursor()
        db = cur.execute
    except psycopg2.DatabaseError as err:
        if con:
            con.rollback()
        print(err)


def get_db():
    if not (con and cur and db):
        connect()
    return (con, cur, db)
