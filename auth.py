from flask import Blueprint, render_template, redirect, url_for,request
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    


    return render_template('login.html')
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    
    if not user or user.password != password:
        return redirect(url_for('auth.signup'))  # Redirect back to login if authentication fails

    login_user(user)
    return redirect(url_for('main.user_patients'))


@auth.route('/signup')
def signup():
  
    
    return render_template('signup.html')

@auth.route('/signup_post', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    

   # print(email, name, password)

    user = User.query.filter_by(email=email).first()
    if user:
        print("user already exist")
    else:
        new_user = User(email=email,password=password,name=name)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('auth.login'))
@ auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
