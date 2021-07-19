from flask import Blueprint, render_template, request, redirect, abort
from flask.helpers import url_for
from flask_login import login_required, logout_user, login_user
from models import User
from urllib.parse import urlparse, urljoin

from dotenv import load_dotenv
import atexit
from flask_login import login_required, current_user
from flask_login import LoginManager

# from db2Api.users import createUser


blog = Blueprint('blog', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@blog.route("/blogs")
def blogs():
    # TODO:fectch all blogs
    return render_template("blog/blog.html")

@blog.route("/add_blog")
@login_required
def composeBlog():
    #TODO: fetch details from blog and store them in DB
    return render_template("blog/add_blog.html")

@blog.route("/read_blog")
def readBlog():
    #TODO:fetch blog detail
    return render_template('blog/readBlog.html')