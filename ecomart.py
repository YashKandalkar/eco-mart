import os
from flask import Flask, flash, render_template, request, redirect, session
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
    from blogs import blog as blog_blueprint
    from models import User
    from db2Api.products \
        import addToCartPost, getProductsbyCategory, getProductsUsingEmail, \
        getAllProducts, createProducts, getProductUsingId, \
        updateProduct, deleteProduct, getSellerName,\
        buyProduct, displayOrders, updateUserPoints,\
        deleteFromCart, cartItemsUsingEmailid, calculateCart,\
        buyCartItems, getProduct, updateCartDetails,\
        givePointsToUser, deleteAllCartItems, getSellerInfo
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
app.register_blueprint(blog_blueprint)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("You have to be logged in to access this page.")
    # TODO: Bug when user is not logged in and tries to access the buy now page,
    # disabled `next` for now
    return redirect(url_for('auth.login', ))


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
    product_detail = getProductsbyCategory(category)
    print(product_detail)

    return render_template('index.html', current_user=user, products=product_detail)

@app.route('/seller/<string:emailId>')
def seller_details(emailId):
    user = current_user if current_user.is_authenticated else None
    seller = getSellerInfo(emailId)
    # TODO: add new attributes to the users db table, modify getSellerDetail function as per db, redirect user to seller_detail.html page
    return render_template('sellerprofile.html', seller= seller)


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
        flash("New product added!")
        return redirect(url_for('.dashboard'))

    else:
        return render_template('add_product.html')


@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    deleteProduct(id)
    flash("Product Deleted!")
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
        # rows = getProductsUsingEmail(current_user.emailid)
        product_detail = getProductUsingId(id)

        flash("Product details updated!")
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
        print('buyer has logged in ')
        orders = displayOrders(current_user.emailid)
        return render_template('dashboard.html', current_user=current_user, orders=orders)

    elif current_user.category == 'Admin':
        return render_template('dashboard.html')

    elif current_user.category == "buyer" and (request.method == 'POST'):
        return render_template('add_recycling_product.html')

    else:
        print("ERROR AYAAAA", current_user.category.strip(),)


@app.route("/products/<id>", methods=['GET'])
@app.route("/products/<id>/", methods=['GET'])
@app.route("/products/<id>/<title>", methods=['GET'])
def products(id, title=None):
    product = getProductUsingId(id)
    dbTitle = product[3].replace(" ", "-").lower()

    if title == None or title != dbTitle:
        if not id:
            return redirect(f"{id}/{dbTitle}")
        else:
            return redirect(f"{dbTitle}")

    seller = getSellerName(id)
    return render_template("product.html", product=product, seller=seller)


@app.route("/products")
@app.route("/products/")
def productsWithNoId():
    return redirect(url_for("index"))


@app.route('/addToCart/<int:id>', methods=['GET', 'POST'])
@login_required
def add_to_cart_post(id):
    if (current_user.category == 'buyer') and (request.method == 'POST'):
        product_detail = getProductUsingId(id)
        quantity = request.form.get('quantity', '')
        quantity = int(quantity)
        rowAdded = addToCartPost(current_user.emailid,
                                 product_detail[0], quantity, product_detail[6])
        cartQuantity = session.get('cart', 0)
        if rowAdded:
            session['cart'] = cartQuantity + 1
        else:
            session['cart'] = cartQuantity
        return redirect(url_for('.cart'))
    else:
        return redirect(url_for('.dashboard'))


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    # if user updates the cart details
    if (current_user.category == 'buyer') and (request.method == 'POST'):
        quantity = request.form.get('updated-quantity', '')
        total_price = request.form.get('total-price', '')
        cart_Id = request.form.get('cartId', '')
        print(quantity, total_price)
        updateCartDetails(cart_Id, quantity, total_price)

    # fetching all cart items
    products = cartItemsUsingEmailid(current_user.emailid)

    return render_template('cart.html', products=products, current_user=current_user)


@app.route('/add_recycling_product', methods=['GET', 'POST'])
@login_required
def add_recycling_product():
    print(current_user.category)
    if (current_user.category == 'buyer') and (request.method == 'POST'):
        product_name = request.form.get('productname', '')
        category = request.form.get('category', '')
        description = request.form.get('description', '')
        quantity = request.form.get('quantity', '')
        seller_emailid = current_user.emailid
        image_url = request.form.get('image_url', '')

        createProducts(seller_emailid, product_name, category,
                       description, image_url, 0, quantity)
        quantity = int(quantity)
        givePointsToUser(quantity, current_user.emailid)
        return redirect(url_for('.dashboard'))
    elif current_user.category == "buyer":
        return render_template("add_recycling_product.html")
    else:
        return redirect(url_for('.index'))


@app.route('/cartBilling', methods=['POST'])
@login_required
def cartBillingView():
    cart_products = cartItemsUsingEmailid(current_user.emailid)
    total_price, total_points = calculateCart(cart_products)
    return render_template('billing.html', products=cart_products, total_price=total_price, total_points=total_points, cart=True)


@app.route('/buyCart', methods=['POST'])
@login_required
def buyAllCartItems():
    # to buy all cart items
    if (current_user.category == 'buyer') and (request.method == 'POST'):
        remaining_points = request.form.get('remaining_points', '')
        updateUserPoints(remaining_points=remaining_points,
                         emailid=current_user.emailid)
        cart_products = cartItemsUsingEmailid(current_user.emailid)
        buyCartItems(cart_products=cart_products)
        deleteAllCartItems(current_user.emailid)
        return redirect(url_for('.dashboard'))


@app.route('/buynow/<int:id>', methods=['POST'])
@login_required
def buynowView(id):

    # buying a asingle item from product/id path
    if (current_user.category == 'buyer') and (request.method == 'POST'):
        quantity = request.form.get('quantity', '')
        quantity = int(quantity)
        products = getProduct(id, current_user.emailid, quantity)
        total_price, total_points = calculateCart(products)
        print(total_points, total_price)
        return render_template("billing.html", products=products, total_price=total_price, total_points=total_points, cart=False)
    else:
        return redirect(url_for('.dashboard'))


@app.route('/buy', methods=['POST'])
@login_required
def buySingleProduct():

    if (current_user.category == 'buyer') and (request.method == 'POST'):
        product_id = request.form.get('product_id', '')
        quantity = request.form.get('quantity', '')
        remaining_points = request.form.get('remaining_points', '')
        price = request.form.get('price', '')
        customer_emailid = request.form.get('user_emailid', '')
        price = int(price)
        quantity = int(quantity)
        print(remaining_points)
        updateUserPoints(remaining_points=remaining_points,
                         emailid=customer_emailid)
        buyProduct(product_id=product_id, customer_emailid=customer_emailid,
                   quantity=quantity, price=price)
        return redirect(url_for('.dashboard'))


@app.route('/deleteCartItem/<int:id>', methods=['POST'])
@login_required
def deleteOneCartItem(id):
    # deleting a cart item from product.html page (using delete button )
    if (current_user.category == 'buyer') and (request.method == 'POST'):
        deleteFromCart(id, current_user.emailid)
        cartQuantity = session.get('cart', 0)
        session['cart'] = max(cartQuantity - 1, 0)
        print("done")
        return redirect(url_for('.cart'))


@app.route('/eco-friendly-business', methods=['GET'])
def ecoFriendlyBusiness():

    return render_template('eco-friendly-business.html')


port = os.getenv('PORT', '5000')
env = os.getenv("FLASK_ENV", "production")


@atexit.register
def shutdown():
    if con:
        con.close()


if __name__ == "__main__":
    app.run(host='localhost' if env == "development" else '0.0.0.0',
            port=int(port), debug=(env == "development"))
