from flask import Blueprint, render_template,request,flash,redirect,url_for

from flask_login import login_required, current_user

from .models import Patient,db
from .models import User
import torch
import numpy as np
from .model import Model

main = Blueprint('main', __name__)
input_dim = 13
model = Model(input_dim)
model.load_state_dict(torch.load('model.pth'))
model.eval()  # Set model to evaluation mode

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
@main.route('/new')
@login_required
def new_patient():
    return render_template('create_patient.html')
@main.route('/new', methods=['POST'])
@login_required
def new_patient_post():
    name = request.form['name']
    age = request.form['age']
    sex = request.form['sex']
    cp = request.form['cp']
    trestbps = request.form['trestbps']
    chol = request.form['chol']
    fbs = request.form['fbs']
    restecg = request.form['restecg']
    thalach = request.form['thalach']
    exang = request.form['exang']
    oldpeak = request.form['oldpeak']
    slope = request.form['slope']
    ca = request.form['ca']
    thal = request.form['thal']

    features = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
    features_tensor = torch.tensor([features], dtype=torch.float32)
    with torch.no_grad():  # No need to compute gradients
        outputs = model(features_tensor)
        target = outputs.item()
    new_entry = Patient(
        name=name,
        age=age,
        sex=sex,
        cp=cp,
        trestbps=trestbps,
        chol=chol,
        fbs=fbs,
        restecg=restecg,
        thalach=thalach,
        exang=exang,
        oldpeak=oldpeak,
        slope=slope,
        ca=ca,
        thal=thal,
        target=target,
        user_id = current_user.id
    )

    db.session.add(new_entry)
    db.session.commit()

    flash('Your workout has been added!')

    return redirect(url_for('main.user_patients'))


@main.route('/all')
@login_required
def user_patients():
    # Fetch the user based on current_user's email
    user = User.query.filter_by(email=current_user.email).first_or_404()

    # Get all patients related to the user
    patients = user.patients

    # Render the template with the patient's data
    return render_template('all_patients.html', patients=patients, user=user)