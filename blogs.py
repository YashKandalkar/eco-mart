from flask import Blueprint, render_template, request, redirect, abort
from flask.helpers import url_for
from flask_login import login_required, logout_user, login_user
from models import User
from urllib.parse import urlparse, urljoin

from dotenv import load_dotenv
import atexit
from flask_login import login_required, current_user
from flask_login import LoginManager

from blogs_defn import addNewBlogPost, getAllBlogs, fetchBlog
from pprint import pprint

# from db2Api.users import createUser


blog = Blueprint('blog', __name__)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@blog.route("/blogs")
def blogs():
    blogs = getAllBlogs()
    # print(blogs)
    return render_template("blog/blog.html", blogs=blogs)


@blog.route("/add_blog", methods=['POST', 'GET'])
@login_required
def addBlog():

    if current_user.category == 'Admin' and (request.method == 'POST'):
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        sub_title = request.form.get('sub-title', '')
        sub_description = request.form.get('sub-description', '')
        thumbnail = request.form.get('thumbnail', '')
        # print(current_user.emailid, len(current_user.emailid), title, description, sub_title, sub_description, thumbnail)
        addNewBlogPost(admin_emailid=current_user.emailid, title=title, description=description,
                       sub_title=sub_title, sub_description=sub_description, thumbnail=thumbnail)
        return redirect(url_for('.blogs'))

    elif current_user.category == 'Admin':
        return render_template("blog/add_blog.html")

    else:
        return redirect(url_for('.blogs'))


@blog.route("/read_blog/<int:id>")
def readBlog(id):

    blog = fetchBlog(id)
    pprint(blog)
    return render_template('blog/readblog.html', blog=blog)
