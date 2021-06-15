# pylint: disable=maybe-no-member

from flask_login import UserMixin
import ibm_db
import os
import json


db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
db2cred = db2info["credentials"]


class User(UserMixin):
    def __init__(self, id, emailid, password, contact_no, firstname, lastname, category, address):
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
        db2conn = ibm_db.pconnect(db2cred['ssldsn'], "", "")
        sql = "SELECT * FROM users WHERE emailid=?"

        stmt = ibm_db.prepare(db2conn, sql)
        ibm_db.bind_param(stmt, 1, emailid)
        try:
            if ibm_db.execute(stmt):
                result = ibm_db.fetch_assoc(stmt)
                if result:
                    result = {k.lower(): result[k] for k in result}
                    return cls(**result)
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(e)
            return None

    @classmethod
    def get(cls, id):
        db2conn = ibm_db.pconnect(db2cred['ssldsn'], "", "")
        sql = "SELECT * FROM users WHERE id=?"

        stmt = ibm_db.prepare(db2conn, sql)
        ibm_db.bind_param(stmt, 1, id)

        try:
            if ibm_db.execute(stmt):
                result = ibm_db.fetch_assoc(stmt)

                if result:
                    result = {k.lower(): result[k] for k in result}
                    return cls(**result)
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(e)
            return None
