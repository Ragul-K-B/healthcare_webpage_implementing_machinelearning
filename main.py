from flask import Blueprint, render_template, request, flash, redirect, url_for
import os
from flask_login import login_required, current_user

from .models import Patient, db
from .models import User
import torch
import numpy as np
from .model import Model

main = Blueprint('main', __name__)
input_dim = 13

# Load the trained model
model_path = 'model.pth'
if os.path.isfile(model_path):
    model = Model(input_dim)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
else:
    raise FileNotFoundError(
        f"The model.pth file was not found at {model_path}. Make sure it's in the correct directory.")


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
    # Retrieve form data
    features = [
        float(request.form['age']),
        float(request.form['sex']),
        float(request.form['cp']),
        float(request.form['trestbps']),
        float(request.form['chol']),
        float(request.form['fbs']),
        float(request.form['restecg']),
        float(request.form['thalach']),
        float(request.form['exang']),
        float(request.form['oldpeak']),
        float(request.form['slope']),
        float(request.form['ca']),
        float(request.form['thal'])
    ]

    features_tensor = torch.tensor([features], dtype=torch.float32)

    # Make prediction
    with torch.no_grad():  # No need to compute gradients
        outputs = model(features_tensor)
        target = outputs.item()

    # Create new Patient entry
    new_entry = Patient(
        name=request.form['name'],
        age=request.form['age'],
        sex=request.form['sex'],
        cp=request.form['cp'],
        trestbps=request.form['trestbps'],
        chol=request.form['chol'],
        fbs=request.form['fbs'],
        restecg=request.form['restecg'],
        thalach=request.form['thalach'],
        exang=request.form['exang'],
        oldpeak=request.form['oldpeak'],
        slope=request.form['slope'],
        ca=request.form['ca'],
        thal=request.form['thal'],
        target=target,
        user_id=current_user.id
    )

    db.session.add(new_entry)
    db.session.commit()

    flash('Your patient data has been added!')
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
