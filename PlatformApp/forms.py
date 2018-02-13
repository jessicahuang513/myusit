from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo,\
    url, ValidationError


#TODO: Add remember me button in index.html

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    #submit = SubmitField('')

class SignUpForm(Form):
    firstName = StringField('')
    lastName = StringField('')
    setEmail = StringField('')
    setEID = StringField('')
    setPassword = PasswordField('')
    setPassword2 = PasswordField('')

class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordForm(Form):
    password = PasswordField('Email', validators=[DataRequired()])
