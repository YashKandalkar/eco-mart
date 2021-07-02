# pylint: disable=maybe-no-member

import os
import json
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
def getAllProducts(con=None, cur=None, db=None):
    sql = "SELECT * FROM products"

    rows = []

    db(sql)
    rows = cur.fetchall()
    return rows or []

@useDb(defaultReturn=0)
def assignPoints(category, con=None, cur=None, db=None):
    # print ('reached')
    if(category == 'Artifacts'):
        return 5
    elif category == 'Furniture':
        return 20
    elif category == 'Clothes':
        return 10
    elif category == 'Bags':
        return 5

@useDb(defaultReturn=False)
def createProducts(emailid, product_name, category, description, image_url,  price, quantity, con=None, cur=None, db=None):
    """
    Tries to create a new product with the given data.

    Returns:
        - list: list  containing all product data, if query was successful
        - False: If query was unsuccessful
    """
    points= assignPoints(category);
    
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
    rows=[]
    sql = "SELECT products.product_id, products.seller_emailid, users.emailid, users.firstname, users.lastname FROM products INNER JOIN users ON (products.seller_emailid=users.emailid) AND products.product_id = %s;"
    db(sql, (id, ))
    if not sql:
        print ('error in executing join query!')
    rows = cur.fetchall()
    return rows or []
    
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
    return rows or []


@useDb(defaultReturn=False)
def updateProduct(seller_emailid, id, product_name, category, description, image_url, price, quantity, con=None, cur=None, db=None):
    """
    Tries to update existing product with the given data.

    Returns:
        - perform updating operation
        - False: If query was unsuccessful
    """

    sql = "UPDATE products SET product_name = %s, product_category= %s, image_path =%s, description=%s, price=%s, quantity=%s WHERE product_id=%s "
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
