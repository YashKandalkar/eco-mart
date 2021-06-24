# pylint: disable=maybe-no-member

from flask_login import UserMixin
import os
import json

from db2Api.users import getUserUsingEmail

from db_connect import get_db

con, cur, db = get_db()


class User(UserMixin):
    def __init__(self, id, emailid, firstname, lastname, password, contact_no,  category, address):
        self.id = id
        self.emailid = emailid
        self.password = password
        self.contact_no = contact_no
        self.firstname = firstname
        self.lastname = lastname
        self.category = category
        self.address = address

    @classmethod
    def getUserFromEmail(cls, emailid):
        result = getUserUsingEmail(emailid)

        if result:
            return cls(*result)
        else:
            return None

    @classmethod
    def get(cls, id):
        sql = "SELECT * FROM users WHERE id=%s"

        try:
            db(sql, (id, ))

            result = cur.fetchone()

            if result:
                return cls(*result)
            else:
                return None
        except Exception as e:
            print(e)
            return None
