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

bp = Blueprint("dish", __name__, url_prefix="/dish")

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

@bp.route("/mydishes")
def mydishes():
    return render_template("dish/mydishes.html")

@bp.route("/addDish",methods=("GET", "POST"))
def addDish():
    if request.method == "POST" :
        name = request.form["name"]
        price = request.form["price"]
        desc = request.form["description"]
        typ = request.form["type"]
        db = get_db()
        price = int(price)
        print(type(price))
        db.execute(
            "INSERT INTO item (name,sellerUsername,price,description,type) VALUES (?,?,?,?,?)",
            (name,g.user['username'],price,desc,typ),
        )
        db.commit()
        return redirect(url_for("dish.mydishes"))
    return render_template("dish/addDish.html")