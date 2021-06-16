# pylint: disable=maybe-no-member

import os
from flask import Flask, render_template
import json
import ibm_db
from dotenv import load_dotenv
import atexit
from flask_login import login_required, current_user
from flask_login import LoginManager

load_dotenv("./.env.local")

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
    db2cred = db2info["credentials"]
    appenv = json.loads(os.environ['VCAP_APPLICATION'])
    db2conn = ibm_db.pconnect(db2cred['ssldsn'], "", "")

    from auth import auth as auth_blueprint
    from models import User
    app.register_blueprint(auth_blueprint)
    login_manager = LoginManager()
    login_manager.init_app(app)
else:
    raise ValueError('Expected cloud environment')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    user = current_user if current_user.is_authenticated else None
    return render_template('index.html', current_user=user)


@app.route('/dashboard')
@login_required

def dashboard():
    if(current_user.category == 'seller'):
        #print('seller has logged in ')
        rows=display_products()
    return render_template('dashboard.html', current_user=current_user,products=rows)

def display_products():
    print('products will be displayed')
    rows=[]
    try:
        db2conn = ibm_db.pconnect(db2cred['ssldsn'], "", "")
        if db2conn:
   
            sql = "SELECT * FROM products where user_emailid=?"

            stmt = ibm_db.prepare(db2conn, sql)

            ibm_db.bind_param(stmt, 1, current_user.emailid)


            if ibm_db.execute(stmt):
                print('query executed')

            else:
                print('query not executed')
                # return render_template('auth/signup.html', error="Error creating an account! Please fill the form and submit again!")
            # close database connection
            result = ibm_db.fetch_assoc(stmt)
            while result != False:  # result is found
                print('rows are appended')
                
                rows.append(result.copy())  #copy the result and append it to rows list
                result = ibm_db.fetch_assoc(stmt)
          # close database connection
            print(rows[0])
            ibm_db.close(db2conn)
            return rows
            # return redirect(url_for('dashboard'))

    except Exception as e:
        print(e)
        errorMsg = ibm_db.conn_errormsg()
        print(errorMsg)
        return render_template('auth/signup.html', error="Error creating an account! Please fill the form and submit again!")


port = os.getenv('PORT', '5000')
env = os.getenv("FLASK_ENV", "production")


@atexit.register
def shutdown():
    if ibm_db.active(db2conn):
        ibm_db.close(db2conn)


if __name__ == "__main__":
    app.run(host='localhost' if env == "development" else '0.0.0.0',
            port=int(port), debug=(env == "development"))
