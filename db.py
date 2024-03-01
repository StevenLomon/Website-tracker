from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    url = db.Column(db.String(240), unique=False, nullable=False)
