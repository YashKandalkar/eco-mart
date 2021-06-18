# pylint: disable=maybe-no-member

from typing import Union
import ibm_db
import os
import json

db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
db2cred = db2info["credentials"]


def createUser(emailid, password, contact_no, firstname, lastname, category, address):
    """
    Tries to create a new user with the given data.

    Returns:
        - dict: dict object containing all user data, if query was successfull
        - False: If query was unsuccessfull
    """

    try:
        db2conn = ibm_db.pconnect(db2cred['ssldsn'], "", "")
        if db2conn:
            # we have a Db2 connection, query the database
            sql = "Insert into users(emailid, password,firstname,lastname,contact_no, category,address ) values (?,?,?,?,?,?,?)"

            stmt = ibm_db.prepare(db2conn, sql)

            ibm_db.bind_param(stmt, 1, emailid)
            ibm_db.bind_param(stmt, 2, password)
            ibm_db.bind_param(stmt, 3, firstname)
            ibm_db.bind_param(stmt, 4, lastname)
            ibm_db.bind_param(stmt, 5, contact_no)
            ibm_db.bind_param(stmt, 6, category)
            ibm_db.bind_param(stmt, 7, address)

            if ibm_db.execute(stmt):
                print('query executed')

            else:
                print('user exist')
                return False
            # close database connection
            ibm_db.close(db2conn)
        else:
            return False
        user = getUserUsingEmail(emailid)
        return user or False

    except Exception as e:
        print(e)
        errorMsg = ibm_db.conn_errormsg()
        print(errorMsg)
        return False


def getUserUsingEmail(emailid) -> Union[dict, None]:
    db2conn = ibm_db.pconnect(db2cred['ssldsn'], "", "")
    sql = "SELECT * FROM users WHERE emailid=?"

    stmt = ibm_db.prepare(db2conn, sql)
    ibm_db.bind_param(stmt, 1, emailid)
    try:
        if ibm_db.execute(stmt):
            result = ibm_db.fetch_assoc(stmt)
            if result:
                result = {k.lower(): result[k] for k in result}
                return result
            else:
                return None
        else:
            return None
    except Exception as e:
        print(e)
        return None
