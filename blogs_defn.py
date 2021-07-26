from db_connect import useDb


@useDb(defaultReturn=False)
def addNewBlogPost(admin_emailid, title, description, sub_title, sub_description, thumbnail, con=None, cur=None, db=None):
    """
    Adds given blog with admin's emailid
    """
    sql = """Insert into blogs(
        admin_emailid,
        title,
        description,
        subtitle,
        sub_description,
        thumbnail
    ) values (%s,%s,%s,%s,%s,%s)"""

    db(sql, (admin_emailid,
             title,
             description,
             sub_title,
             sub_description,
             thumbnail
             ))
    con.commit()

@useDb(defaultReturn=False)
def getAllBlogs(con=None, cur=None, db=None):
    """
    gets all blog details
    Returns:
        - rows: all blogs as list
        - [] : if no blogs are present in db
    """
    sql = "SELECT * FROM blogs ORDER BY id ASC"

    rows = []

    db(sql, ( ))
    rows = cur.fetchall()
    return rows or []

@useDb(defaultReturn=False)
def fetchBlog(blog_id , con=None, cur=None, db=None):
    """
    Fetches a blog for given blog_id
    Returns : 
        -row[0]: tuple that contain a blog info
        - () : empty tuple if it fails  
    """
    sql = """ SELECT * FROM  blogs WHERE id = %s """
    rows = []
    db(sql, (blog_id,))
    rows = cur.fetchall()
    return rows[0] or ()
