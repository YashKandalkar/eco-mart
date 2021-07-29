from flask import Blueprint, render_template, request, redirect, abort, session
from flask.helpers import flash, url_for
from flask_login import login_required, logout_user, login_user
from models import User
from urllib.parse import urlparse, urljoin


from db2Api.users import createUser
from db2Api.products import getCartItemsQuantity


auth = Blueprint('auth', __name__)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


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

        login_user(user, remember=remember)
        session['cart'] = getCartItemsQuantity(user.emailid)
        print(session['cart'])
        next = request.form.get('next')

        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('index'))


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
            user = User(*result)
            login_user(user, remember=remember)
            session['cart'] = 0
            next = request.form.get('next')

            if not is_safe_url(next):
                return abort(400)

            flash("signup")
            return redirect(next or url_for('index'))
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
