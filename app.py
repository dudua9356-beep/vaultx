from flask import Flask, render_template, request, redirect
import os
from models import db, User

app = Flask(__name__)

# CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "vaultx123")

# INIT DB
db.init_app(app)

# RESET DATABASE (remove tabelas antigas com erro)
with app.app_context():
    db.drop_all()
    db.create_all()

# HOME
@app.route("/")
def home():
    users = User.query.all()
    return render_template("index.html", users=users)

# CRIAR USUÁRIO
@app.route("/create", methods=["POST"])
def create_user():
    username = request.form.get("username")

    if username:
        user = User(username=username, balance=1000)
        db.session.add(user)
        db.session.commit()

    return redirect("/")

# ADICIONAR SALDO
@app.route("/add/<int:user_id>")
def add_balance(user_id):
    user = User.query.get(user_id)

    if user:
        user.balance += 100
        db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run()
