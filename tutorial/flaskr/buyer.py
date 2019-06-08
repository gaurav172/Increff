import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.db import get_db

bp = Blueprint("buyer", __name__, url_prefix="/buyer")

def login_required(view):
    """View decorator that
    redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )

@bp.route("/order")
def order():
    db = get_db()
    userList = ( get_db().execute("SELECT username FROM user", ).fetchall() )
    userDict = {}
    # print(size(userList))
    for x in userList:
        # print(x[0])
        userDict[x[0]]= ( get_db().execute("SELECT name FROM sell WHERE sellerUsername = ?", (x[0],)).fetchall() )
    g.uDict = userDict
    # print(userDict)
    return render_template("buyer/order.html")

@bp.route("/menu<uname>")
def menu(uname):
    g.seller = uname
    g.userDish = ( get_db().execute("SELECT * FROM item WHERE sellerUsername=?", (uname,) ).fetchall() )
    return render_template("buyer/menu.html")
