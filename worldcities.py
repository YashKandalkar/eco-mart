# pylint: disable=maybe-no-member

import os
from flask import Flask, redirect, render_template, request
import urllib
import datetime
import json
import ibm_db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
    db2cred = db2info["credentials"]
    appenv = json.loads(os.environ['VCAP_APPLICATION'])
else:
    raise ValueError('Expected cloud environment')

# handle database request and query city information


def city(name=None):
    # connect to DB2
    rows = []
    try:
        db2conn = ibm_db.connect(db2cred['ssldsn'], "", "")
        if db2conn:
            # we have a Db2 connection, query the database
            sql = "select * from cities where name=? order by population desc"
            # Note that for security reasons we are preparing the statement first,
            # then bind the form input as value to the statement to replace the
            # parameter marker.
            stmt = ibm_db.prepare(db2conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.execute(stmt)
            # fetch the result
            result = ibm_db.fetch_assoc(stmt)
            while result != False:  # result is found
                # copy the result and append it to rows list
                rows.append(result.copy())
                result = ibm_db.fetch_assoc(stmt)
            # close database connection
            ibm_db.close(db2conn)
        # passing the rows list (it contains result of query)
        return render_template('city.html', ci=rows)
    except:
        app.logger.error('could not establish Db2 connection')
        errorMsg = ibm_db.conn_errormsg()
        app.logger.error(errorMsg)
        return render_template('city.html', ci=[])


# main page to dump some environment information
@app.route('/')
def index():
    return render_template('index.html', app=appenv)

# for testing purposes - use name in URI


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/search', methods=['GET'])
def searchroute():
    name = request.args.get('name', '')
    return city(name)


@app.route('/city/<name>')
def cityroute(name=None):
    return city(name)


@app.route('/gallery')
def galleryroute():
    return render_template("gallery.html")


port = os.getenv('PORT', '5000')
env = os.getenv("FLASK_ENV", "production")
if __name__ == "__main__":
    app.run(host='localhost', port=int(port), debug=(env == "development"))
