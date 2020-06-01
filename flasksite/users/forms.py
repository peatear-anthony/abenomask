from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flasksite.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    first_name = StringField('First Name',
                            validators=[DataRequired()])

    last_name = StringField('Last Name',
                            validators=[DataRequired()])

    postal_code = StringField('Postal Code',
                            validators=[DataRequired()])

    prefecture = StringField('Prefecture',
                            validators=[DataRequired()])

    my_number = StringField('My Number',
                            validators=[Length(min=1, max=12)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):   
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('That email is already taken. Please choose a different one.')


    def validate_mynumber(self, email):   
        my_number = User.query.filter_by(my_number=my_number.data).first()

        if my_number:
            raise ValidationError('That My Number is already taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[ Length(min=2, max=20)])

    first_name = StringField('First Name',
                            validators=[])

    last_name = StringField('Last Name',
                            validators=[])

    postal_code = StringField('Postal Code',
                            validators=[])

    my_number = StringField('My Number',
                            validators=[Length(min=1, max=12)])
    
    prefecture = StringField('Prefecture',
                            validators=[DataRequired()])

    email = StringField('Email',
                        validators=[Email()])

    picture = FileField('Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:   
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is already taken. Please choose a different one.')


    def validate_mynumber(self, email):   
        if my_number.data != current_user.my_number:  
            my_number = User.query.filter_by(my_number=my_number.data).first()
            if my_number:
                raise ValidationError('That My Number is already taken. Please choose a different one.')