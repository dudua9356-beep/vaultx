from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.secret_key = "vaultx-secret-key"

# Banco SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vaultx.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID automático
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=10000.0)

# Criar banco na primeira execução
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return redirect("/login")

# REGISTRO
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "Usuário já existe"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            return redirect("/dashboard")
        else:
            return "Login inválido"

    return render_template("login.html")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    try:
        response = requests.get(
            "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
            timeout=5
        )
        btc_price = response.json()["price"]
    except:
        btc_price = "Indisponível"

    return render_template("dashboard.html", user=user, btc_price=btc_price)

# COMPRA
@app.route("/buy")
def buy():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    user.balance -= 100
    db.session.commit()
    return redirect("/dashboard")

# VENDA
@app.route("/sell")
def sell():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    user.balance += 100
    db.session.commit()
    return redirect("/dashboard")

# ADMIN — adicionar saldo por ID
@app.route("/admin/add/<int:user_id>/<float:amount>")
def add_balance(user_id, amount):
    user = User.query.get(user_id)
    if not user:
        return "Usuário não encontrado"

    user.balance += amount
    db.session.commit()

    return f"Saldo atualizado. Novo saldo: {user.balance}"

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
