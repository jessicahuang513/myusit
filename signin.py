from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from PlatformApp.mainApp import app
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from PlatformApp import db

signe = create_engine('postgresql+psycopg2://signinapp:password@127.0.0.1:5432/signin')

Session = sessionmaker(bind=signe)

signsession = Session()

manager = Manager(app)

class Member(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	eid = db.Column(db.String(8), unique = True)
	firstName = db.Column(db.String(80))
	lastName = db.Column(db.String(80))
	email = db.Column(db.String(80))
	attendance = db.Column(db.Integer)
	dues = db.Column(db.Integer)
	atLatestMeeting = db.Column(db.Boolean)
	rowOnSheet = db.Column(db.Integer)
	comments = db.Column(db.String(80))
	year = db.Column(db.String(80))

	@staticmethod
	def get_by_eid(eid):
		return Member.query.filter_by(eid=eid).first()

	@staticmethod
	def check_attendance(dues, attendance):
		if dues > 45:
			return True
		elif dues == 45:
			return attendance <= num_gms_semester
		elif dues == 0:
			return attendance <= num_gms_free
		return False

@manager.command
def print_users():
	for user in signsession.query(Member).all():
		print(user.email)

@manager.command
def return_all_users_signin():
	return signsession.query(Member).all()

if __name__ == '__main__':
    manager.run()