# pylint: disable=maybe-no-member

import os
from flask import Flask, flash, render_template, request, redirect
import json
from flask.helpers import url_for

from dotenv import load_dotenv
import atexit
from flask_login import login_required, current_user
from flask_login import LoginManager

load_dotenv("./.env.local")

if 'DATABASE_URI' in os.environ:
    from db_connect import get_db
    from auth import auth as auth_blueprint
    from models import User
    from db2Api.products import add_to_cart, getProductsbyCategory, getProductsUsingEmail, getAllProducts, createProducts, getProductUsingId, updateProduct, deleteProduct, getSellerDetail
else:
    raise ValueError('Env Var not found!')

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# get service information if on IBM Cloud Platform


con, cur, db = get_db()

app.register_blueprint(auth_blueprint)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('auth.login', next=request.endpoint))


@app.errorhandler(404)
def not_found_handler(e):
    print(e)
    return render_template("404.html")


@app.route('/')
def index():
    user = current_user if current_user.is_authenticated else None
    rows = getAllProducts()
    return render_template('index.html', current_user=user, products=rows)

@app.route('/<string:category>')
def filter(category):
    user = current_user if current_user.is_authenticated else None
    #todo : fetch products with given categories
    product_detail = getProductsbyCategory(category)
    print(product_detail)

    return render_template('index.html', current_user = user, products = product_detail)

@app.route('/buynow/<int:id>', methods= ['POST'])
# @login_required
def buynow(id):
    user = current_user if current_user.is_authenticated else None
    if (current_user.category == 'buyer') and (request.method == 'POST'):
        quantity = request.form.get('quantity', '')
    product_detail = getProductUsingId(id)
    quantity = int(quantity)
    print(product_detail,quantity)
    return render_template('buynow.html', current_user=user, product= product_detail, quantity= quantity)



@app.route('/addtocart/<int:id>', methods=['POST'])
def add_to_cart(id):

    # product = Product.query.filter(Product.id == product_id)
    product_detail = getProductUsingId(id)
    # cart_item = CartItem(product=product_detail)
    print(product_detail)
    return render_template('addtocart.html', products=product_detail, current_user= current_user)


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if (current_user.category == 'seller') and (request.method == 'POST'):
        product_name = request.form.get('productname', '')
        category = request.form.get('category', '')
        description = request.form.get('description', '')
        price = request.form.get('price', '')
        quantity = request.form.get('quantity', '')
        seller_emailid = current_user.emailid
        image_url = request.form.get('image_url', '')
        createProducts(seller_emailid, product_name, category,
                       description, image_url, price, quantity)
        return redirect(url_for('.dashboard'))
    elif current_user.category == 'seller':
        return render_template("add_product.html")
    else:
        # to-do
        return redirect(url_for('.dashboard'))


@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    deleteProduct(id)
    return redirect(url_for('.dashboard'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_product(id):
    if (current_user.category == 'seller') and (request.method == 'POST'):
        product_name = request.form.get('productname', '')
        category = request.form.get('category', '')
        description = request.form.get('description', '')
        price = request.form.get('price', '')
        quantity = request.form.get('quantity', '')
        seller_emailid = current_user.emailid
        image_url = request.form.get('image_url', '')
        updateProduct(seller_emailid, id, product_name, category,
                      description, image_url, price, quantity)
        rows = getProductsUsingEmail(current_user.emailid)
        product_detail = getProductUsingId(id)
        
        # todo: flash message to indicate --- product details has been updated
        # flash("you are successfully updated product")
        return redirect(url_for('.dashboard'))
    elif (current_user.category == 'seller'):
        product_detail = getProductUsingId(id)
        print(product_detail[0])
        return render_template('update_product.html', current_user=current_user, product=product_detail)
    else:
        # since buyer has no rights to update products detail, he will be redirected to dashboard
        return redirect(url_for('.dashboard'))


# buyer's and seller's dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    category = current_user.category.strip()
    if(category == 'seller'):
        print('seller has logged in ')
        rows = getProductsUsingEmail(current_user.emailid)
        return render_template('dashboard.html', current_user=current_user, products=rows)

    elif category == 'buyer':
        #print('buyer has logged in ')
        return render_template('dashboard.html', current_user=current_user)
    else:
        print("ERROR AYAAAA", current_user.category.strip(),)


@app.route("/products/<id>", methods=['GET'])
@app.route("/products/<id>/", methods=['GET'])
@app.route("/products/<id>/<title>", methods=['GET'])
def products(id, title=None):
    if title == None:
        #work in progress
        # if title == None:
        # TODO: Fetch only product-name from id, redirect to /product/<id>/<title>
        # Replace spaces with dashes TODO: Also urlencode this string
        # (some chars cannot come in a url)
        #  title = "Fetch title from db".replace(" ", "-").lower()
        #  if not id:
        #      return redirect(f"{id}/{title}")
        #  else:
        #      return redirect(f"{title}")
        if title == None or id == None:
            user = current_user if current_user.is_authenticated else None

        return redirect(url_for('.index'))
    else:
        seller = getSellerDetail(id)
        product = getProductUsingId(id)
        # print(product,seller)
        return render_template("product.html", product=product, seller= seller)

    # TODO: Fetch product from id, send details to the frontend
    return render_template("product.html")


@app.route("/products")
def productsWithNoId():
    return redirect(url_for("index"))


@app.route('/addToCart', methods=['GET', 'POST'])
@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    return render_template('cart.html')


port = os.getenv('PORT', '5000')
env = os.getenv("FLASK_ENV", "production")


@atexit.register
def shutdown():
    if con:
        con.close()


if __name__ == "__main__":
    app.run(host='localhost' if env == "development" else '0.0.0.0',
            port=int(port), debug=(env == "development"))
