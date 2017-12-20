from datetime import datetime
from PlatformApp import db, cipher_suite
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import json
import requests
from flask_security import RoleMixin

num_gms_semester = 13
num_gms_free = 2
year_dues = 70
semester_dues = 45


ticker_identifier = db.Table('student_identifier',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('ticker_id', db.Integer, db.ForeignKey('tickers.id'))
)
#required for Flask-Security, could be useful later for admin screen
roles_users = db.Table('roles_users',
		db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
		db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class RecentVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(5))
    close = db.Column(db.Boolean)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(5))
    email = db.Column(db.String(80))
    position = db.Column(db.String(80))

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(5))
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    datetime = db.Column(db.String(80))
    change = db.Column(db.Float)
    percentChange = db.Column(db.Float)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    eid = db.Column(db.String, unique = True)
    firstName = db.Column(db.String(80))
    lastName = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    attendance = db.Column(db.Integer)
    dues = db.Column(db.Integer)
    atLatestMeeting = db.Column(db.Boolean)
    rowOnSheet = db.Column(db.Integer)
    password_hash = db.Column(db.String)
    ret = db.Column(db.Float)
    score = db.Column(db.Float)
    active = db.Column(db.Boolean)
    stocks = db.relationship('Tickers', secondary=ticker_identifier, backref='user')
    transactions = db.relationship('Transactions', backref='user')
    #required for Flask-Security
    roles =  db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # print("HERE IS THE PASSWORD: ", password)
        return check_password_hash(self.password_hash, cipher_suite.decrypt(password).decode())

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_eid(eid):
        return User.query.filter_by(eid = eid).first()

    @staticmethod
    def check_attendance(dues, attendance):
        if dues > semester_dues:
            return True
        elif dues == semester_dues:
            return attendance <= num_gms_semester
        elif dues == 0:
            return attendance <= num_gms_free
        return False

    def __repr__(self):
        return "<User '{}'>".format(self.email)


class Tickers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ticker = db.Column(db.String(5), unique=True)
    ticker = db.Column(db.String(5))
    startingPrice = db.Column(db.Float)
    short = db.Column(db.Boolean)
    #transactions = db.relationship('Transactions', backref='tickers')
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return "<Ticker '{}'>".format(self.ticker)

class Transactions(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticker = db.Column(db.String(5))
    date = db.Column(db.String)
    end_price = db.Column(db.Integer)
    returns = db.Column(db.Integer)

# Flask Security
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
