# pylint: disable=maybe-no-member

import ibm_db
import os
import json
import urllib.request
from werkzeug.utils import secure_filename
from .users import getUserUsingEmail

db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
db2cred = db2info["credentials"]


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def getProductsUsingEmail(emailid) -> list:
    db2conn = ibm_db.pconnect(db2cred['ssldsn'], "", "")
    sql = "SELECT * FROM products WHERE seller_emailid=?"

    rows = []

    stmt = ibm_db.prepare(db2conn, sql)
    ibm_db.bind_param(stmt, 1, emailid)
    try:
        if ibm_db.execute(stmt):
            result = ibm_db.fetch_assoc(stmt)
            while result != False:  # result is found
                # print('rows are appended')

                # copy the result and append it to rows list
                rows.append(result.copy())
                result = ibm_db.fetch_assoc(stmt)
            # print(rows)
            ibm_db.close(db2conn)
            return rows
        else:
            return rows
    except Exception as e:
        print(e)
        errorMsg = ibm_db.conn_errormsg()
        print(errorMsg)
        return rows


def getAllProducts():
    db2conn = ibm_db.pconnect(db2cred['ssldsn'], "", "")
    sql = "SELECT * FROM products"

    rows = []

    stmt = ibm_db.prepare(db2conn, sql)

    try:
        if ibm_db.execute(stmt):
            result = ibm_db.fetch_assoc(stmt)
            while result != False:  # result is found
                # copy the result and append it to rows list
                rows.append(result.copy())
                result = ibm_db.fetch_assoc(stmt)
            ibm_db.close(db2conn)
            return rows
        else:
            return rows
    except Exception as e:
        print(e)
        errorMsg = ibm_db.conn_errormsg()
        print(errorMsg)
        return rows


def createProducts(emailid, product_name, category, description, image_url,  price, quantity):
    """
    Tries to create a new product with the given data.

    Returns:
        - dict: dict object containing all user data, if query was successful
        - False: If query was unsuccessful
    """
    row=[]
    try:
        db2conn = ibm_db.pconnect(db2cred['ssldsn'], "", "")
        if db2conn:
            # we have a Db2 connection, query the database
            # TODO: Add seller_emailid
            sql = "Insert into products(seller_emailid,product_name, product_category,description, image_path, price,quantity) values (?,?,?,?,?,?,?)"

            stmt = ibm_db.prepare(db2conn, sql)

            ibm_db.bind_param(stmt, 1, emailid)
            ibm_db.bind_param(stmt, 2, product_name)
            ibm_db.bind_param(stmt, 3, category)
            ibm_db.bind_param(stmt, 4, description)
            ibm_db.bind_param(stmt, 5, image_url)
            ibm_db.bind_param(stmt, 6, price)
            ibm_db.bind_param(stmt, 7, quantity)
            print('parameters passed')

            if ibm_db.execute(stmt):
                print('query executed')
                result = ibm_db.fetch_assoc(stmt)
                row.append(result.copy())
                print(row)
                return row

            else:
                print('user exist')
                return False
            # close database connection
            ibm_db.close(db2conn)
            
        else:
            return False
        
        return user or False

    except Exception as e:
        print(e)
        errorMsg = ibm_db.conn_errormsg()
        print(errorMsg)
        return False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
