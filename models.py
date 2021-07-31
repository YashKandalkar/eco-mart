from flask_login import UserMixin
import os
import json

from db2Api.users import getUserUsingEmail

from db_connect import useDb


class User(UserMixin):
    def __init__(self, id, emailid, firstname, lastname, password, contact_no,  category, address, points, description, company_url, image_url):
        self.id = id
        self.emailid = emailid
        self.password = password
        self.contact_no = contact_no
        self.firstname = firstname
        self.lastname = lastname
        self.category = category
        self.address = address
        self.points = points
        self.description = description
        self.company_url = company_url
        self.image_url = image_url

    @classmethod
    def getUserFromEmail(cls, emailid):
        result = getUserUsingEmail(emailid)

        if result:
            return cls(*result)
        else:
            return None

    @classmethod
    @useDb()
    def get(cls, id, con=None, cur=None, db=None):
        sql = "SELECT * FROM users WHERE id=%s"

        db(sql, (id, ))

        result = cur.fetchone()

        if result:
            return cls(*result)
        else:
            return None
