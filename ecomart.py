# pylint: disable=maybe-no-member

import os
from flask import Flask, render_template, request, redirect
import json
from flask.helpers import url_for
import ibm_db

from dotenv import load_dotenv
import atexit
from flask_login import login_required, current_user
from flask_login import LoginManager


load_dotenv("./.env.local")


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
    db2cred = db2info["credentials"]
    appenv = json.loads(os.environ['VCAP_APPLICATION'])
    db2conn = ibm_db.pconnect(db2cred['ssldsn'], "", "")

    from auth import auth as auth_blueprint
    from models import User
    from db2Api.products import getProductsUsingEmail, getAllProducts, createProducts
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
    rows = getAllProducts()

    return render_template('index.html', current_user=user, products=rows)


@app.route('/add_product', methods=['GET'])
@login_required
def add_product():
    if(current_user.category == 'seller'):
        # createProducts()
        return render_template('add_product.html', current_user=current_user)
    else:
        # to-do
        return render_template('dashboard.html', current_user=current_user)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        product_name = request.form.get('productname', '')
        category = request.form.get('category', '')
        description = request.form.get('description', '')
        price = request.form.get('price', '')
        quantity = request.form.get('quantity', '')
        # print("everything  worked properly")
        result = createProducts(
            current_user.emailid, product_name, category, description, price, quantity)
        return redirect(url_for('dashboard'))

    else:
        if(current_user.category == 'seller'):
            #print('seller has logged in ')
            rows = getProductsUsingEmail(current_user.emailid)
            return render_template('dashboard.html', current_user=current_user, products=rows)
        #print('buyer has logged in ')
        return render_template('dashboard.html', current_user=current_user)


@app.route("/products/<id>", methods=['GET'])
@app.route("/products/<id>/", methods=['GET'])
@app.route("/products/<id>/<title>", methods=['GET'])
def products(id, title=None):
    if title == None:
        # TODO: Fetch only product-name from id, redirect to /product/<id>/<title>
        # Replace spaces with dashes TODO: Also urlencode this string
        # (some chars cannot come in a url)
        title = "Fetch title from db".replace(" ", "-").lower()
        if not id:
            return redirect(f"{id}/{title}")
        else:
            return redirect(f"{title}")

    # TODO: Fetch product from id, send details to the frontend
    return render_template("product.html")


@app.route("/products")
def productsWithNoId():
    return redirect(url_for("index"))


port = os.getenv('PORT', '5000')
env = os.getenv("FLASK_ENV", "production")


@atexit.register
def shutdown():
    if ibm_db.active(db2conn):
        ibm_db.close(db2conn)


if __name__ == "__main__":
    app.run(host='localhost' if env == "development" else '0.0.0.0',
            port=int(port), debug=(env == "development"))
