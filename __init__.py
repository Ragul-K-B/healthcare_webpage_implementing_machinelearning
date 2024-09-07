import os
import torch
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
model = None  # Global variable to store the model


def load_model(app):
    global model
    model_path = os.path.join(app.root_path, 'model.pth')

    # Debugging statements
    print(f"Root path: {app.root_path}")
    print(f"Model path: {model_path}")
    print(f"File exists: {os.path.isfile(model_path)}")

    if os.path.isfile(model_path):
        model = torch.load(model_path, map_location=torch.device('cpu'))
        print(f"Model loaded from {model_path}")
    else:
        raise FileNotFoundError(f"The model.pth file was not found at {model_path}")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Load the model when the app is created
    load_model(app)

    return app
