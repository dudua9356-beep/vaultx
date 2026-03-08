from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(5), unique=True)
    username = db.Column(db.String(100))
    balance = db.Column(db.Float, default=10000.0)
