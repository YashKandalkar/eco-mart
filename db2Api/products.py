import os
import json
from threading import current_thread
import urllib.request
# from werkzeug.utils import secure_filename
from .users import getUserUsingEmail

from db_connect import useDb


@useDb(defaultReturn=[])
def getProductsUsingEmail(emailid, con=None, cur=None, db=None) -> list:
    sql = "SELECT * FROM products WHERE seller_emailid=%s ORDER BY product_id ASC"

    rows = []

    db(sql, (emailid, ))
    rows = cur.fetchall()
    return rows or []


@useDb(defaultReturn=[])
def getProductsbyCategory(category, con=None, cur=None, db=None):
    """
    Tries to fetch products according to given category eg. Artifacts.

    Returns:
        - list: list  containing given category product data, if query was successful
        - False: If query was unsuccessful
    """
    sql = """SELECT *
            FROM products
            where product_category=%s
            ORDER BY product_id ASC"""

    rows = []

    db(sql, (category,))
    rows = cur.fetchall()
    return rows or []


@useDb(defaultReturn=[])
def addToCartPost(emailid, product_id, quantity, price,  con=None, cur=None, db=None):

    sql1 = """SELECT * FROM cart where emailid = %s and product_id = %s """
    db(sql1, (emailid,
              product_id
              ))
    rows = cur.fetchall()
    # item was not present in the cart
    if len(rows) == 0:
        sql = """Insert into cart(
            emailid,
            product_id,
            quantity,
            price
            
        ) values (%s,%s,%s,%s)"""

        db(sql, (emailid,
                 product_id,
                 quantity,
                 price
                 ))
        con.commit()
    # item is present in the cart
    else:
        sql2 = """UPDATE cart
            SET 
            quantity = quantity+ %s 
            WHERE 
            product_id=%s and 
            emailid= %s """
        db(sql2, (quantity,
                  product_id,
                  emailid
                  ))
        con.commit()


@useDb(defaultReturn=[])
def getAllProducts(con=None, cur=None, db=None):
    sql = "SELECT * FROM products where quantity>=1 and product_category !='Recycling' "

    rows = []

    db(sql)
    rows = cur.fetchall()
    return rows or []


@useDb(defaultReturn=0)
def assignPoints(category, con=None, cur=None, db=None):
    if(category == 'Artifacts'):
        return 5
    elif category == 'Furniture':
        return 20
    elif category == 'Clothes':
        return 10
    elif category == 'Bags':
        return 5
    else :
        return 0


@useDb(defaultReturn=False)
def createProducts(emailid, product_name, category, description, image_url,  price, quantity, con=None, cur=None, db=None):
    """
    Tries to create a new product with the given data.

    Returns:
        - list: list  containing all product data, if query was successful
        - False: If query was unsuccessful
    """
    points = assignPoints(category)

    sql = """Insert into products(
        seller_emailid,
        product_name,
        product_category,
        description,
        image_path,
        price,
        quantity,
        points
    ) values (%s,%s,%s,%s,%s,%s,%s,%s)"""

    db(sql, (emailid,
             product_name,
             category,
             description,
             image_url,
             price,
             quantity,
             points))
    con.commit()


@useDb(defaultReturn=[])
def getSellerDetail(id=id, con=None, cur=None, db=None):
    rows = []
    sql = """SELECT
            products.product_id,
            products.seller_emailid,
            users.emailid,
            users.firstname,
            users.lastname
            FROM products
            INNER JOIN users
            ON
            (products.seller_emailid = users.emailid)
            AND
            products.product_id = %s;"""
    db(sql, (id, ))
    if not sql:
        print('error in executing join query!')
    rows = cur.fetchall()
    return rows or []


@useDb(defaultReturn=False)
def updateUserPoints(remaining_points, emailid, con=None, cur=None, db=None):
    """
    Tries to update users points

    Returns:
        - perform updating operation
        - False: If query was unsuccessful
    """
    sql = """UPDATE users
            SET
            points = %s
            WHERE
            emailid=%s """
    db(sql, (remaining_points,
             emailid
             ))
    con.commit()


@useDb(defaultReturn=False)
def getProductUsingId(id=id, con=None, cur=None, db=None):
    """
    Tries to fetch product data from database.

    Returns:
        - list: list  containing data about the product, if query was successful
        - False: If query was unsuccessful
    """
    rows = []
    sql = "SELECT *  FROM products where product_id = %s"
    db(sql, (id, ))

    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0]
    else:
        return []


@useDb(defaultReturn=False)
def getProduct(id, user_emailid, quantity, con=None, cur=None, db=None):
    rows = []
    sql = "SELECT product_id,product_name, product_category, price, points FROM products where product_id = %s"
    db(sql, (id, ))
    rows = cur.fetchall()
    temp = list(rows[0])
    temp.insert(3, user_emailid)
    temp.insert(4, quantity)
    rows[0] = tuple(temp)
    return rows


@useDb(defaultReturn=False)
def updateProduct(seller_emailid, id, product_name, category, description, image_url, price, quantity, con=None, cur=None, db=None):
    """
    Tries to update existing product with the given data.

    Returns:
        - perform updating operation
        - False: If query was unsuccessful
    """

    sql = """UPDATE products
            SET
            product_name = %s,
            product_category= %s,
            image_path =%s,
            description=%s,
            price=%s,
            quantity=%s
            WHERE
            product_id=%s """
    db(sql, (product_name,
             category,
             image_url,
             description,
             price,
             quantity,
             id,))
    con.commit()


@useDb(defaultReturn=False)
def deleteProduct(id, con=None, cur=None, db=None):
    """
    Tries to delete existing product with the given product_id.

    Returns:
        - perform deleting operation
        - False: If query was unsuccessful
    """
    sql = "DELETE FROM products WHERE product_id=%s"
    db(sql, (id, ))
    con.commit()


@useDb(defaultReturn=False)
def buyProduct(product_id, customer_emailid, quantity, price, con=None, cur=None, db=None):
    """
    Tries to buy a product with the given data.

    Returns:
        - perform insert operation in orders table
        - False: If query was unsuccessful
    """
    sql = """INSERT INTO orders (
        customer_emailid,
        product_id,
        quantity,
        price
        )
        values(%s,%s,%s,%s)"""
    db(sql, (customer_emailid,
             product_id,
             quantity,
             price*quantity))
    con.commit()
    updateInventory(product_id, quantity)


@useDb(defaultReturn=[])
def displayOrders(customer_emailid, con=None, cur=None, db=None):
    """
    Tries to display orders placed by specified user.

    Returns:
        - list: list  containing data about the product, if query was successful
        - empty list: user have never placed a single order
    """
    rows = []
    sql = """
    SELECT
    products.product_id,
    orders.product_id,
    products.product_name,
    products.product_category,
    orders.customer_emailid,
    orders.quantity,
    orders.price
    FROM products
    INNER JOIN orders
    ON orders.customer_emailid = %s AND products.product_id = orders.product_id"""
    db(sql, (customer_emailid, ))
    rows = cur.fetchall()
    return rows or []


@useDb(defaultReturn=False)
def deleteFromCart(id, emailid, con=None, cur=None, db=None):
    """
    Tries to delete selected product from cart.

    Returns:
        - perform deleting operation
        - False: If query was unsuccessful
    """
    sql = "DELETE FROM cart WHERE id=%s and emailid=%s"
    db(sql, (id, emailid, ))
    con.commit()


@useDb(defaultReturn=False)
def CartItemsUsingEmailid(emailid, con=None, cur=None, db=None):
    sql = """
    SELECT
    products.product_id,
    products.product_name,
    products.description,
    cart.emailid,
    cart.quantity,
    cart.price,
    products.points,
    products.image_path,
    cart.id,
    products.quantity,
    products.price
    FROM products
    INNER JOIN cart
    ON cart.emailid = %s AND products.product_id = cart.product_id
    """

    rows = []

    db(sql, (emailid, ))
    rows = cur.fetchall()
    return rows or []


@useDb(defaultReturn=False)
def getCartItemsQuantity(emailid, con=None, cur=None, db=None):
    """
    Tries to fetch number of products in cart.

    Returns:
        - int: number of products in cart
        - False: If query was unsuccessful
    """
    sql = """
    SELECT
    COUNT(*)
    FROM cart
    WHERE emailid = %s
    """
    db(sql, (emailid, ))
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return 0


@useDb(defaultReturn=False)
def calculateCart(cart_products, con=None, cur=None, db=None):
    total_price = total_points = 0
    for product in cart_products:
        total_price += product[4] * product[5]
        total_points += product[4] * product[6]
    return total_price, total_points


@ useDb(defaultReturn=False)
def buyCartItems(cart_products, con=None, cur=None, db=None):
    for product in cart_products:
        sql = """INSERT INTO orders (
            customer_emailid,
            product_id,
            quantity,
            price
            )
            values(%s,%s,%s,%s)"""
        db(sql, (product[3],
                 product[0],
                 product[4],
                 product[4]*product[5]))
        con.commit()
        updateInventory(product[0], product[4])

        deleteFromCart(product[0], product[3])


@ useDb(defaultReturn=False)
def updateInventory(product_id, quantity_purchased, con=None, cur=None, db=None):
    sql = """UPDATE products
            SET
            quantity= quantity - %s
            WHERE
            product_id=%s """
    db(sql, (
        quantity_purchased,
        product_id,))
    con.commit()


@ useDb(defaultReturn=False)
def updateCartDetails(cart_id, new_quantity, price_per_product, con=None, cur=None, db=None):
    sql = """UPDATE cart
            SET
            quantity= %s,
            price = %s
            WHERE
            id=%s """
    db(sql, (
        new_quantity,
        price_per_product,
        cart_id,))
    con.commit()

@ useDb(defaultReturn=False)
def givePointsToUser( quantity, user_emailid, con=None, cur=None, db=None):
    if quantity > 2:
        sql = """UPDATE users
                SET
                points= points + 10
                WHERE
                emailid=%s """
    else :
        
        sql = """UPDATE users
                SET
                points= points + 5
                WHERE
                emailid=%s """

    db(sql, (
        user_emailid,
        ))
    con.commit()
    