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
    return render_template('all_patients.html', patients=patients,user=user)
@main.route('/patient/<int:patient_id>/delete', methods=['GET'])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('main.user_patients'))
@main.route("/patient/<int:patient_id>/patient", methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if request.method == 'POST':
        # Collect the updated form data
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

        # Log the collected form data for debugging
        print("Form data collected:", features)

        # Convert the features into a tensor for model prediction
        features_tensor = torch.tensor([features], dtype=torch.float32)

        # Log the tensor data for debugging
        print("Features tensor created:", features_tensor)

        # Make prediction using the preloaded model
        with torch.no_grad():
            outputs = model(features_tensor)
            target = outputs.item()

        # Log the prediction for debugging
        print("Predicted target:", target)

        # Update patient data in the database
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.sex = request.form['sex']
        patient.cp = request.form['cp']
        patient.trestbps = request.form['trestbps']
        patient.chol = request.form['chol']
        patient.fbs = request.form['fbs']
        patient.restecg = request.form['restecg']
        patient.thalach = request.form['thalach']
        patient.exang = request.form['exang']
        patient.oldpeak = request.form['oldpeak']
        patient.slope = request.form['slope']
        patient.ca = request.form['ca']
        patient.thal = request.form['thal']
        patient.target = target  # Update the target value with the new prediction

        # Log the updated patient data for debugging
        print("Updated patient data:", patient)

        # Commit to database
        db.session.commit()

        # Log confirmation of commit
        print("Database updated successfully")

        flash('Patient information updated successfully!')
        return redirect(url_for('main.user_patients'))

    return render_template('edit_patient.html', patient=patient)
