import os
from dotenv import load_dotenv
import psycopg2
import traceback

load_dotenv("./.env.local")

con = cur = db = None

if 'DATABASE_URI' in os.environ:
    DATABASE_URL = os.environ['DATABASE_URI']
else:
    raise ValueError('Env Var not found!')


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


def get_db(force=False):
    if force:
        con.rollback()
        return (con, cur, db)
    if not (con and cur and db):
        connect()
    return (con, cur, db)


def useDb(defaultReturn=None):
    def wrapper(func=None):
        def inner(*args, **kwargs):
            con, cur, db = get_db()
            if "retrying" in kwargs and kwargs["retrying"]:
                try:
                    print("Retrying query")
                    del kwargs["retrying"]
                    kwargs.update({"con": con, "cur": cur, "db": db, })
                    return func(*args, **kwargs)
                except:
                    print(traceback.format_exc())
                    print(defaultReturn)
                    return defaultReturn

            try:
                kwargs.update({"con": con, "cur": cur, "db": db, })
                return func(*args, **kwargs)
            except psycopg2.DatabaseError:
                print(traceback.format_exc())
                if "retrying" in kwargs:
                    raise RuntimeError("Fatal Error occured!")
                else:
                    con, cur, db = get_db(force=True)
                    return inner(*args, **kwargs, retrying=True)
            except:
                print(traceback.format_exc())
                return defaultReturn

        return inner
    return wrapper
