# pylint: disable=maybe-no-member

import os
from flask import Flask, redirect, render_template, request
import urllib
import datetime
import json
from flask.helpers import url_for
import ibm_db
from dotenv import load_dotenv

load_dotenv("./.env.local")

app = Flask(__name__)

# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
    db2cred = db2info["credentials"]
    appenv = json.loads(os.environ['VCAP_APPLICATION'])
else:
    raise ValueError('Expected cloud environment')


def signup(emailid, password, contact_no, firstname, lastname, category, address):
    try:
        db2conn = ibm_db.connect(db2cred['ssldsn'], "", "")
        if db2conn:
            ci = {"firstname": firstname, "lastname": lastname}

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
            # close database connection
            ibm_db.close(db2conn)
        # passing the rows list (it contains result of query)
        return redirect(url_for('user', usr=firstname))
    except Exception as e:
        app.logger.error('could not establish Db2 connection')
        print(e)
        errorMsg = ibm_db.conn_errormsg()
        app.logger.error(errorMsg)
        return render_template('signup.html', error="Error creating an account! Please fill the form and submit again!")


@app.route('/')
def index():
    return render_template('index.html', app=appenv)


# signup page
@app.route('/signup', methods=['GET', 'POST'])
def signuproute():
    if request.method == 'POST':
        emailid = request.form.get('emailid', '')
        password = request.form.get('password', '')
        contact_no = request.form.get('contact_no', '')
        firstname = request.form.get('firstname', '')
        lastname = request.form.get('lastname', '')
        category = request.form.get('category', '')
        address = request.form.get('address', '')
        return signup(emailid, password, contact_no, firstname, lastname, category, address)
    else:
        return render_template('signup.html')


@app.route('/<usr>')
def user(usr):
    return render_template('dashboard.html', usr=usr)


port = os.getenv('PORT', '5000')
env = os.getenv("FLASK_ENV", "production")

if __name__ == "__main__":
    app.run(host='localhost' if env == "development" else '0.0.0.0',
            port=int(port), debug=(env == "development"))
