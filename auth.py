# pylint: disable=maybe-no-member

from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for
from flask_login import login_required, logout_user, login_user
from models import User

from db2Api.users import createUser


auth = Blueprint('auth', __name__)


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
        remember = request.form.get('remember', '')
        result = createUser(emailid, password, contact_no,
                            firstname, lastname, category, address)
        if result:
            user = User(**result)
            login_user(user, remember=remember)
            return redirect(url_for('dashboard'))
        else:
            return render_template('auth/signup.html',
                                   error="Error creating an account! Please fill the form and submit again!")
    else:
        return render_template('auth/signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
