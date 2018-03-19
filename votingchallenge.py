from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, backref, relationship
from PlatformApp.models import Tickers, Role, Transactions, Stock, Vote, RecentVote, AnalystFile, FundFile
from PlatformApp import db
from PlatformApp.mainApp import app
from flask_script import Manager
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

votee = create_engine('postgresql+psycopg2://byciwgzypwngid:password@127.0.0.1:5432/votingchallenge')

Session = sessionmaker(bind=votee)

votesession = Session()

manager = Manager(app)

ticker_identifier = Table('student_identifier', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('ticker_id', Integer, ForeignKey('tickers.id'))
)
#required for Flask-Security, could be useful later for admin screen
roles_users = Table('roles_users', Base.metadata,
		Column('user_id', Integer(), ForeignKey('user.id')),
		Column('role_id', Integer(), ForeignKey('role.id'))
)

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	firstName = Column(String(80))
	lastName = Column(String(80))
	email = Column(String(80), unique=True)
	password_hash = Column(String)
	ret = Column(Float)
	score = Column(Float)
	active = Column(Boolean)
	# stocks = relationship('Tickers', secondary=ticker_identifier, backref='user')
	# transactions = relationship('Transactions', backref='user')
	# roles =  relationship('Role', secondary=roles_users, backref=backref('users', lazy='dynamic'))

	@property
	def password(self):
		return self.password_hash

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, cipher_suite.decrypt(password).decode())

	@staticmethod
	def get_by_email(email):
		return User.query.filter_by(email=email).first()

	def __repr__(self):
		return "<User '{}'>".format(self.email)

# @manager.command
# def print_users():
# 	for stock in votesession.query(Tickers).all():
# 		print(stock.ticker)

def get_users_from_vote():
	return votesession.query(User).all()

def get_ticker_identifier():
	return votesession.query(ticker_identifier).all()

def get_roles_users():
	return votesession.query(roles_users).all()

@manager.command
def print_types():
	for transaction in votesession.query(Transactions).all():

@manager.command
def get_non_user_data():
	print("Avoid error string.")

	# for stock in votesession.query(Stock).all():
	# 	try:
	# 		db.session.add(Stock(id = stock.id,
	# 							 ticker = stock.ticker,
	# 							 name = stock.name,
	# 							 price = stock.price,
	# 							 datetime = stock.datetime,
	# 							 change = stock.change,
	# 							 percentChange = stock.percentChange))
	# 		db.session.commit()
	# 		print("Added " + stock.ticker)
	# 	except:
	# 		print("Doesn't work.")

	# for ticker in votesession.query(Tickers).all():
	# 	try:
	# 		db.session.add(Tickers(id = ticker.id,
	# 							  ticker = ticker.ticker,
	# 							  startingPrice = ticker.startingPrice,
	# 							  short = ticker.short))
	# 		db.session.commit()
	# 		print("Added " + ticker.ticker)
	# 	except:
	# 		print("Doesn't work.")

	for transaction in votesession.query(Transactions).all():
		try:
			db.session.add(Transactions(id = transaction.id,
										user_id = transaction.user_id,
										ticker = transaction.ticker,
										date = transaction.date,
										end_price = transaction.end_price,
										returns = transaction.returns))
			db.session.commit()
			print("Added " + transaction.ticker + " " + transaction.user_id)
		except Exception as e:
			print("Doesn't work.")
			print(e)

	# for role in votesession.query(Role).all():
	# 	try:
	# 		if role.id != 1:
	# 			db.session.add(Role(id = role.id,
	# 								name = role.name,
	# 								description = role.description))
	# 			db.session.commit()
	# 			print("Added " + role.name)
	# 		else:
	# 			print("Admin already exists so didn't add it again!")
	# 	except Exception as e:
	# 		print("Doesn't work.")
	# 		print(e)

if __name__ == '__main__':
	manager.run()
