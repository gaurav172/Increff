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

@bp.route("/menu<uname>",methods=("GET", "POST"))
def menu(uname):
    db= get_db()
    g.seller = uname
    g.userDish = (  get_db().execute("SELECT * FROM item WHERE sellerUsername=?", (uname,) ).fetchall() )
    if request.method == "POST" :
        dishes = request.form.getlist('name')
        buyerName = g.user["username"]
        sellerName = uname
        status = "Pending"
        time = 1 #get time using python date and time
        date = 1 #get date "   "
        total_cost = 1
        quantity =1 
        db.execute(
            "INSERT INTO orderhistory (buyerName,sellerName,status,price,date,time) VALUES (?,?,?,?,?,?)",
            (buyerName,sellerName,status,total_cost,time,date)
        )
        db.commit()
        bid = (db.execute("SELECT max(orderid) FROM orderhistory").fetchone())
        bid = bid[0]      
        for x in dishes:       
            quantity = 1
            price = 1
            db.execute(
                "INSERT INTO orderdish (orderid,itemName,price,qty) VALUES (?,?,?,?)",
                (bid,x,price,quantity)
            )
            db.commit()
        return redirect(url_for("buyer.order"))
    return render_template("buyer/menu.html")


@bp.route("/meal<id>",methods=("GET","POST"))
def meal(id):
    if request.method == "POST":
        seats = request.form["seats"]
        db = get_db()
        ml = (db.execute("SELECT * FROM meal WHERE buffetNo=?",(id,)).fetchone())
        db.execute(
            "INSERT INTO buffethistory (invName,joName,total,price,date,time) VALUES (?,?,?,?,?,?)",
            (ml["inviterName"],g.user["username"],seats,int(seats)*int(ml["price"]),"date","time")
        )
        db.commit()
    db = get_db()
    g.meal = (db.execute("SELECT * FROM meal WHERE buffetNo=?",(id,)).fetchone())
    g.Menu = (db.execute("SELECT * FROM buffetdishes WHERE buffetNo=?",(id,)).fetchall())
    return render_template("buyer/meal.html")

@bp.route("/joinMeal")
def joinMeal():
    db = get_db()
    userList = ( db.execute("SELECT username FROM user", ).fetchall() )
    userDict = {}
    for x in userList:
        userDict[x[0]] = (db.execute("SELECT * FROM meal WHERE inviterName = ?",(x[0],)).fetchall())
    g.mealDict = userDict
    return render_template("buyer/joinMeal.html")

