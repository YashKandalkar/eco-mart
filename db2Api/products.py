# pylint: disable=maybe-no-member

import os
import json
import urllib.request
# from werkzeug.utils import secure_filename
from .users import getUserUsingEmail

from db_connect import get_db


def getProductsUsingEmail(emailid) -> list:
    sql = "SELECT * FROM products WHERE seller_emailid=%s ORDER BY product_id ASC"

    rows = []

    try:
        con, cur, db = get_db()
        db(sql, (emailid, ))
        rows = cur.fetchall()
        return rows or []
    except Exception as e:
        print(e)
        return rows


def getAllProducts():
    sql = "SELECT * FROM products"

    rows = []

    try:
        con, cur, db = get_db()
        db(sql)
        rows = cur.fetchall()
        print(rows)
        return rows or []
    except Exception as e:
        print(e)
        return rows


def createProducts(emailid, product_name, category, description, image_url,  price, quantity):
    """
    Tries to create a new product with the given data.

    Returns:
        - list: list  containing all product data, if query was successful
        - False: If query was unsuccessful
    """
    try:
        sql = """Insert into products(
            seller_emailid,
            product_name, 
            product_category,
            description,
            image_path,
            price,
            quantity
        ) values (%s,%s,%s,%s,%s,%s,%s)"""

        con, cur, db = get_db()

        db(sql, (emailid,
                 product_name,
                 category,
                 description,
                 image_url,
                 price,
                 quantity))
        print((emailid,
               product_name,
               category,
               description,
               image_url,
               price,
               quantity))
        con.commit()

    except Exception as e:
        print(e)
        return False


def getProductUsingId(id=id):
    """
    Tries to fetch product data from database.

    Returns:
        - list: list  containing data about the product, if query was successful
        - False: If query was unsuccessful
    """
    rows = []
    try:
        sql = "SELECT *  FROM products where product_id = %s"
        con, cur, db = get_db()
        db(sql, (id, ))

        rows = cur.fetchall()
        return rows or []
    except Exception as e:
        print(e)
        return False


def updateProduct(seller_emailid, id, product_name, category, description, image_url, price, quantity):
    """
    Tries to update existing product with the given data.

    Returns:
        - perform updating operation
        - False: If query was unsuccessful
    """

    try:

        sql = "UPDATE products SET product_name = %s, product_category= %s, image_path =%s, description=%s, price=%s, quantity=%s WHERE product_id=%s "
        con, cur, db = get_db()
        db(sql, (product_name,
                 category,
                 image_url,
                 description,
                 price,
                 quantity,
                 id,))
        con.commit()

    except Exception as e:
        print(e)
        return False


def deleteProduct(id):
    """
    Tries to delete existing product with the given product_id.

    Returns:
        - perform deleting operation
        - False: If query was unsuccessful
    """
    try:
        con, cur, db = get_db()
        sql = "DELETE FROM products WHERE product_id=%s"
        db(sql, (id, ))
        con.commit()

    except Exception as e:
        print(e)
        return False
