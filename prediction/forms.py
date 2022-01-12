from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, DecimalField, RadioField, SubmitField, StringField, PasswordField, SelectField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from prediction.models import User
import pickle

class PredictionForm(FlaskForm):
    highBP = BooleanField(label='Czy masz wysokie ciśnienie tętnicze? (powyżej 140/90)')
    highChol = BooleanField(label='Czy masz wysoki cholesterol? (powyżej 180)')
    cholCheck = BooleanField(label='Czy w ciągu ostatnich 5 lat był badany poziom cholesterolu?')
    bmi = DecimalField(label='Podaj BMI (waga w kilogramach/wzrost do kwadratu(w metrach) {np. 78/1,98})', validators=[DataRequired()])
    smoker = BooleanField(label='Czy wypaliłes przynajmniej 100 papierosów w swoim życiu?')
    stroke = BooleanField(label='Czy miałeś kiedykolwiek zdiagnozowany udar?')
    heartDiseaseOrAttack = BooleanField(label='Czy przechodziłes zawał serca?')
    physActivity = BooleanField(label='Czy w ciągu ostatniego miesiąc uprawiałes jakąś aktywność fizyczna poza pracą?')
    fruits = BooleanField(label='Czy jesz owoce przynajmniej raz dziennie?')
    veggies = BooleanField(label='Czy jesz warzywa przynajmniej raz dziennie?')
    alcConsumption = BooleanField(label='Czy wypijasz więcej niz 7 drinków tygodniowo? (mężczyźni 14 drinków)')
    mentalHealth = IntegerField(
        label='Przez ile dni w ciągu ostatniego miesiąca miałeś obciążenie psychiczne? (stres, depresja, problemy emocjonalne itp...)', validators=[DataRequired()])
    sex = RadioField(label='Podaj płeć', coerce=int, choices=[('0', 'Kobieta'), ('1', 'Mężczyzna')], validators=[DataRequired()])
    age = IntegerField(label='Podaj wiek')
    age = SelectField(label='Podaj wiek',
                      choices=[(0, '18 - 24 lat'), (1, '25 - 29 lat'), (2, '30 - 34 lat'), (3, '35 - 39 lat'),
                               (4, '40 - 44 lat'), (5, '45 - 49 lat'), (6, '50 - 54 lat'), (7, '55 - 59 lat'),
                               (8, '60 - 64 lat'), (9, '65 - 69 lat'),(10, '70 - 74 lat'),(11, '75 - 79 lat'),(12, '80 i więcej lat')])
    education = SelectField(label='Podaj wykształcenie',
                            choices=[(1,'nie ukończyłem szkoły podstawowej'), (2,'skończyłem szkołę podstawową'), (3,'średnie bez matury'), (4,'średnie z maturą'), (5,'licencjat/inżynier'), (6,'wyższe (co najmniej magisterskie)')])
    submit = SubmitField(label='Sprawdź czy masz cukrzycę...')

    def prediction(dataToPredict):
        filename = "model_diabetes.hdf5"
        model = pickle.load(open(filename, 'rb'))
        result = model.predict(dataToPredict)
        probability = model.predict_proba(dataToPredict)
        probability = "{0:.2f}".format(probability[0][int(result)] * 100)
        return result, probability

class RegistrationForm(FlaskForm):
    def validate_username(self, inputUsername):
        user = User.query.filter_by(username=inputUsername.data).first()
        if user:
            raise ValidationError('Nazwa użytkownika jest już zajęta! Spróbuje ponownie.')

    def validate_email_address(self, inputEmail):
        user = User.query.filter_by(email=inputEmail.data).first()
        if user:
            raise ValidationError('Podany przez Ciebie adres email istnieje już w bazie. Tylko jedno konto może być połączone z adresem email')

    username = StringField(label='Nazwa użytkownika', validators=[Length(min=3, max=30), DataRequired()])
    email_address = StringField(label='Adres Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Hasło', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Potwierdź Hasło', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Stwórz Konto')

class LoginForm(FlaskForm):
    username = StringField(label='Nazwa Użytkownika', validators=[DataRequired()])
    password = PasswordField(label='Hasło', validators=[DataRequired()])
    submit = SubmitField(label='Zaloguj się')