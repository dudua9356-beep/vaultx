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


# pegar preços das criptomoedas
def get_prices():

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin,ethereum,ripple,tron",
        "vs_currencies": "usd"
    }

    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        return data
    except:
        return {}


# página inicial
@app.route("/")
def index():

    prices = get_prices()
    users = User.query.all()

    return render_template(
        "dashboard.html",
        prices=prices,
        users=users
    )


# login simples
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]

    user = User.query.filter_by(username=username).first()

    if not user:
        user = User(username=username, balance=1000)

        db.session.add(user)
        db.session.commit()

    return redirect("/")


# dashboard
@app.route("/dashboard")
def dashboard():

    prices = get_prices()
    users = User.query.all()

    return render_template(
        "dashboard.html",
        prices=prices,
        users=users
    )


# login admin
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        password = request.form["password"]

        if password == "vaultxadmin123":

            users = User.query.all()

            return render_template(
                "admin_panel.html",
                users=users
            )

    return render_template("admin_login.html")


if __name__ == "__main__":
    app.run()
