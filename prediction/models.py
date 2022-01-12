from prediction import db, login_manager
from prediction import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class PatientData(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=True)
    diabetes = db.Column(db.Integer(), nullable=True)
    highBP = db.Column(db.Boolean(), nullable=False)
    highChol = db.Column(db.Boolean(), nullable=False)
    bmi = db.Column(db.Numeric(3,2), nullable=False)
    smoker = db.Column(db.Boolean(), nullable=False)
    stroke = db.Column(db.Boolean(), nullable=False)
    heartDiseaseOrAttack = db.Column(db.Boolean(), nullable=False)
    physActivity = db.Column(db.Boolean(), nullable=False)
    fruits = db.Column(db.Boolean(), nullable=False)
    veggies = db.Column(db.Boolean(), nullable=False)
    alcConsumption = db.Column(db.Boolean(), nullable=False)
    mentalHealth = db.Column(db.Integer(), nullable=False)
    sex = db.Column(db.Boolean(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    education = db.Column(db.Integer(), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    patientDatas = db.relationship('PatientData', backref='user_data', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, inputPassword):
        self.password_hash = bcrypt.generate_password_hash(inputPassword).decode('utf8')

    def checkPassword(self, inputPaasword):
        return bcrypt.check_password_hash(self.password_hash, inputPaasword)
