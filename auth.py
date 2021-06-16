# pylint: disable=maybe-no-member

from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for
from flask_login import login_required, logout_user
import ibm_db
from models import User
from flask_login import login_user
import os
import json

auth = Blueprint('auth', __name__)
db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
db2cred = db2info["credentials"]


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('auth/login.html')
    else:
        emailid = request.form.get('emailid', '')
        password = request.form.get('password', '')
        remember = True if request.form.get('remember') else False

        user = User.getUserFromEmail(emailid)
        if not user or not user.password == password:
            print("WRONG PASS, NO USER")
            return render_template('auth/login.html', error="Wrong email or password, please try again!")

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('dashboard'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        emailid = request.form.get('emailid', '')
        password = request.form.get('password', '')
        contact_no = request.form.get('contact_no', '')
        firstname = request.form.get('firstname', '')
        lastname = request.form.get('lastname', '')
        category = request.form.get('category', '')
        address = request.form.get('address', '')
        return createUser(emailid, password, contact_no, firstname, lastname, category, address)
    else:
        return render_template('auth/signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def createUser(emailid, password, contact_no, firstname, lastname, category, address):
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
                return render_template('auth/signup.html', error="Error creating an account! Please fill the form and submit again!")
            # close database connection
            ibm_db.close(db2conn)
        return redirect(url_for('dashboard'))

    except Exception as e:
        print(e)
        errorMsg = ibm_db.conn_errormsg()
        print(errorMsg)
        return render_template('auth/signup.html', error="Error creating an account! Please fill the form and submit again!")
