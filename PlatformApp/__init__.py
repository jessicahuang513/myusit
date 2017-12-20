import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail
from cryptography.fernet import Fernet
import smtplib

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)	
app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'platform.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['DEBUG'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_REGISTERABLE'] = True
db = SQLAlchemy(app)

app.config['PYTHONHTTPSVERIFY'] = 0

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "index"
login_manager.init_app(app)


# Configure new user email settings
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('votingchallenge@usiteam.org', 'votingchallenge2016')

# Configure Flask Mail
mail=Mail(app)

key = Fernet.generate_key()
cipher_suite = Fernet(key)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=587,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'votingchallenge@usiteam.org',
	MAIL_PASSWORD = 'votingchallenge2016'
	)

mail=Mail(app)

import models
import mainApp
