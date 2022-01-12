from prediction import app, db
from flask import render_template, redirect, url_for, flash, request
from prediction.models import PatientData, User
from prediction.forms import PredictionForm, RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
import datetime


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/predict', methods=['GET', 'POST'])
def prediction_page():
    form = PredictionForm()
    if request.method == 'POST':
        newPatientData = PatientData()
        newPatientData.date = datetime.datetime.now()
        newPatientData.highBP = form.highBP.data
        newPatientData.highChol = form.highChol.data
        newPatientData.bmi = form.bmi.data
        newPatientData.smoker = form.smoker.data
        newPatientData.stroke = form.stroke.data
        newPatientData.heartDiseaseOrAttack = form.heartDiseaseOrAttack.data
        newPatientData.physActivity = form.physActivity.data
        newPatientData.fruits = form.fruits.data
        newPatientData.veggies = form.veggies.data
        newPatientData.alcConsumption = form.alcConsumption.data
        newPatientData.mentalHealth = form.mentalHealth.data
        newPatientData.sex = form.sex.data
        newPatientData.age = form.age.data
        newPatientData.education = form.education.data

        predictionData = [[form.highBP.data, form.highChol.data, form.bmi.data,
                           form.smoker.data, form.stroke.data, form.heartDiseaseOrAttack.data,
                           form.physActivity.data, form.fruits.data, form.veggies.data, form.alcConsumption.data,
                           form.mentalHealth.data, form.sex.data, form.age.data, form.education.data]]
        result, probability = PredictionForm.prediction(predictionData)
        msg = ""
        if (result == 0):
            category = 'success'
            msg = f'Na {probability}% Nie masz cukrzycy.'
        elif (result == 1):
            category = 'danger'
            msg = f'Na {probability}% Masz stan przedcukrzycowy!'
        else:
            category = 'danger'
            msg = f'Na {probability}% Masz Cukrzycę !!!!'
        flash(msg, category=category)
    return render_template('guest.html', form=form)


@app.route('/user/prediction', methods=['GET', 'POST'])
@login_required
def user_page():
    form = PredictionForm()
    if request.method == 'POST':
        newPatientData = PatientData()
        newPatientData.user = current_user.id
        newPatientData.date = datetime.datetime.now()
        newPatientData.highBP = form.highBP.data
        newPatientData.highChol = form.highChol.data
        newPatientData.bmi = form.bmi.data
        newPatientData.smoker = form.smoker.data
        newPatientData.stroke = form.stroke.data
        newPatientData.heartDiseaseOrAttack = form.heartDiseaseOrAttack.data
        newPatientData.physActivity = form.physActivity.data
        newPatientData.fruits = form.fruits.data
        newPatientData.veggies = form.veggies.data
        newPatientData.alcConsumption = form.alcConsumption.data
        newPatientData.mentalHealth = form.mentalHealth.data
        newPatientData.sex = form.sex.data
        newPatientData.age = form.age.data
        newPatientData.education = form.education.data

        predictionData = [[form.highBP.data, form.highChol.data, form.bmi.data,
                           form.smoker.data, form.stroke.data, form.heartDiseaseOrAttack.data,
                           form.physActivity.data, form.fruits.data, form.veggies.data, form.alcConsumption.data,
                           form.mentalHealth.data, form.sex.data, form.age.data, form.education.data]]

        result, probability = PredictionForm.prediction(predictionData)
        newPatientData.diabetes = int(result)

        msg = ""
        if (result == 0):
            category = 'success'
            msg = f'Na {probability}% Nie masz cukrzycy.'
        elif (result == 1):
            category = 'danger'
            msg = f'Na {probability}% Masz stan przedcukrzycowy!'
        else:
            category = 'danger'
            msg = f'Na {probability}% Masz Cukrzycę !!!!'

        db.session.add(newPatientData)
        db.session.commit()
        flash(msg, category=category)
        return redirect(url_for('userData_page'))
    return render_template('user.html', form=form)

@app.route('/user/data')
@login_required
def userData_page():
    storedData = PatientData.query.filter_by(user=current_user.id)
    return render_template('userData.html',storedData=storedData)

@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        newUser = User(username=form.username.data, email=form.email_address.data, password=form.password1.data)
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser)
        flash(f'Zostałeś poprawnie zalogowany jako: {newUser.username}', category='success')
        return redirect(url_for('user_page'))
    if form.errors:
        for error in form.errors.values():
            flash(f'Wystąpił bład podczas tworzeia nowego konta: {error}', category='danger')
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.checkPassword(inputPaasword=form.password.data):
            login_user(user)
            flash(f'Zostałeś poprawnie zalogowany jako: {user.username}', category='success')
            return redirect(url_for('user_page'))
        else:
            flash(f'Hasło lub nazwa użytkownika zostały podane niepoprawnie. Spróbuj ponownie', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('Zostałes poprawnie wylogowany', category='info')
    return redirect(url_for('home_page'))