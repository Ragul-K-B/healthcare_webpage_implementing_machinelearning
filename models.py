from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    patients = db.relationship('Patient', backref='author', lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    cp = db.Column(db.Integer, nullable=False)
    trestbps = db.Column(db.Integer, nullable=False)
    chol = db.Column(db.Integer, nullable=False)
    fbs = db.Column(db.Integer, nullable=False)
    restecg = db.Column(db.Integer, nullable=False)
    thalach = db.Column(db.Integer, nullable=False)
    exang = db.Column(db.Integer, nullable=False)
    oldpeak = db.Column(db.Float, nullable=False)
    slope = db.Column(db.Integer, nullable=False)
    ca = db.Column(db.Integer, nullable=False)
    thal = db.Column(db.Integer, nullable=False)
    target = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
