from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random, os

app = Flask(__name__)
app.secret_key = "super-secret-key"

# Banco de dados (mesma URL do admin)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(5), unique=True)  # ID aleatório de 5 dígitos
    username = db.Column(db.String(100))
    balance = db.Column(db.Float, default=10000.0)

# Cria tabelas se não existirem
with app.app_context():
    db.create_all()

# Página principal / dashboard
@app.route("/")
def dashboard():
    # Pega o primeiro usuário cadastrado só para demo
    user = User.query.first()
    if not user:
        return "Nenhum usuário criado ainda!"
    return render_template("dashboard.html", user=user)

# Criar usuário
@app.route("/create", methods=["POST"])
def create_user():
    username = request.form.get("username")
    if not username:
        return "Informe um nome de usuário!"

    # Gera ID aleatório de 5 dígitos e garante que seja único
    while True:
        user_id = str(random.randint(10000, 99999))
        if not User.query.filter_by(user_id=user_id).first():
            break

    new_user = User(username=username, user_id=user_id)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run()
