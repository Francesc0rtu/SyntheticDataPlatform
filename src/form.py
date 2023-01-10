from flask_wtf import FlaskForm
from wtforms import MultipleFileField, StringField, SubmitField, PasswordField, validators
from wtforms.validators import DataRequired



class Login(FlaskForm):
    name = StringField( 'Username', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')

class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField(label='Email', validators=[
        DataRequired(),
        # validators.Length(min=1, max=35),
        validators.Email()
    ])
    password = PasswordField(label='Password', validators=[
        DataRequired(),
        # validators.Length(min=1, max=10),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField(label='Password confirm', validators=[
        DataRequired()
        # validators.Length(min=1, max=10)
    ])

class Upload(FlaskForm):
    files = MultipleFileField('Upload File')
    dataset_name = StringField('Dataset Name', validators=[DataRequired()])
    submit = SubmitField('Upload')
    