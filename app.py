import os
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "vaultx_secret"

# Banco PostgreSQL do Render
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///vaultx.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= MODELOS =================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    balance = db.Column(db.Float, default=10000.0)

# ================= ROTAS =================

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    user = User.query.get(session["user_id"])
    return render_template("dashboard.html", user=user)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session["user_id"] = user.id
            return redirect("/")
    return render_template("login.html")

@app.route("/buy")
def buy():
    user = User.query.get(session["user_id"])
    user.balance -= 100
    db.session.commit()
    return redirect("/")

@app.route("/sell")
def sell():
    user = User.query.get(session["user_id"])
    user.balance += 100
    db.session.commit()
    return redirect("/")

@app.route("/admin-9482", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        user_id = request.form["user_id"]
        amount = float(request.form["amount"])
        user = User.query.get(user_id)
        if user:
            user.balance += amount
            db.session.commit()
    users = User.query.all()
    return render_template("admin.html", users=users)

# ================= RUN =================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
