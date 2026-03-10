from flask import Flask, render_template, request, redirect
from models import db, User
import requests
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "vaultx_secret"

db.init_app(app)

with app.app_context():
    db.create_all()


def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin,ethereum,ripple,tron",
        "vs_currencies": "usd"
    }

    r = requests.get(url, params=params)
    return r.json()


@app.route("/")
def dashboard():

    prices = get_prices()
    users = User.query.all()

    return render_template(
        "dashboard.html",
        prices=prices,
        users=users
    )


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        user = User(username=username, balance=1000)

        db.session.add(user)
        db.session.commit()

        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        user = User.query.filter_by(username=username).first()

        if user:
            return redirect("/")

    return render_template("login.html")


@app.route("/admin")
def admin():

    users = User.query.all()

    return render_template("admin.html", users=users)


if __name__ == "__main__":
    app.run()
