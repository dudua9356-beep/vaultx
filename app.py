from flask import Flask, render_template, redirect
import requests

app = Flask(__name__)

# Usuário fake temporário
class User:
    def __init__(self):
        self.id = 1
        self.balance = 10000.0

user = User()

@app.route("/")
def home():
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            timeout=5
        )
        data = response.json()
        btc_price = data["bitcoin"]["usd"]
    except:
        btc_price = "Indisponível"

    return render_template(
        "dashboard.html",
        user=user,
        btc_price=btc_price
    )

@app.route("/buy")
def buy():
    user.balance -= 100
    return redirect("/dashboard")

@app.route("/sell")
def sell():
    user.balance += 100
    return redirect("/dashboard")

@app.route("/admin-9482")
def admin():
    return "Área Admin"

if __name__ == "__main__":
    app.run(debug=True)
