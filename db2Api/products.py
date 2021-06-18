# pylint: disable=maybe-no-member

import ibm_db
import os
import json

db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
db2cred = db2info["credentials"]


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
                print('rows are appended')

                # copy the result and append it to rows list
                rows.append(result.copy())
                result = ibm_db.fetch_assoc(stmt)
            print(rows)
            ibm_db.close(db2conn)
            return rows
        else:
            return rows
    except Exception as e:
        print(e)
        errorMsg = ibm_db.conn_errormsg()
        print(errorMsg)
        return rows
