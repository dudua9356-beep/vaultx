from flask import Flask, render_template, request, redirect, session
from .config import Config
from .models import db, User
import random

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def generate_id():
    return str(random.randint(10000,99999))

@app.before_first_request
def create_tables():

    db.create_all()

    if User.query.count() == 0:

        user = User(
            user_id=generate_id(),
            username="TraderDemo",
            balance=10000
        )

        db.session.add(user)
        db.session.commit()

@app.route("/")
def dashboard():

    user = User.query.first()

    return render_template("dashboard.html", user=user)

@app.route("/buy")
def buy():

    user = User.query.first()

    if user.balance >= 100:
        user.balance -= 100
        db.session.commit()

    return redirect("/")

@app.route("/sell")
def sell():

    user = User.query.first()

    user.balance += 100
    db.session.commit()

    return redirect("/")

@app.route("/admin", methods=["GET","POST"])
def admin_login():

    if request.method == "POST":

        password = request.form["password"]

        if password == app.config["ADMIN_PASSWORD"]:
            session["admin"] = True
            return redirect("/admin_panel")

    return render_template("admin_login.html")

@app.route("/admin_panel", methods=["GET","POST"])
def admin_panel():

    if "admin" not in session:
        return redirect("/admin")

    users = User.query.all()

    if request.method == "POST":

        user_id = request.form["user_id"]
        amount = float(request.form["amount"])

        user = User.query.filter_by(user_id=user_id).first()

        if user:
            user.balance += amount
            db.session.commit()

    return render_template("admin_panel.html", users=users)
