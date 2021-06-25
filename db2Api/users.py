# pylint: disable=maybe-no-member

from typing import Union
import os
import json

from db_connect import get_db

con, cur, db = get_db()


def createUser(emailid, password, contact_no, firstname, lastname, category, address):
    """
    Tries to create a new user with the given data.

    Returns:
        - dict: dict object containing all user data, if query was successfull
        - False: If query was unsuccessful
    """

    try:

        sql = """Insert into users(
            emailid, 
            password,
            firstname,
            lastname,
            contact_no, 
            category,
            address 
        ) values (%s,%s,%s,%s,%s,%s,%s)"""
        db(sql, (emailid,
                 password,
                 firstname,
                 lastname,
                 contact_no,
                 category,
                 address))
        con.commit()
        # close database connection
        user = getUserUsingEmail(emailid)
        return user or False

    except Exception as e:
        print(e)
        return False


def getUserUsingEmail(emailid) -> Union[dict, None]:
    sql = "SELECT * FROM users WHERE emailid=%s"

    try:
        db(sql, (emailid, ))
        rows = cur.fetchone()

        return rows
    except Exception as e:
        print(e)
        return None