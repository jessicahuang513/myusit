from PlatformApp.mainApp import app, db, update_ret, add_stock, update_score, create_stock_info
from PlatformApp.models import User, Tickers, Role, Transactions, Stock, Vote, RecentVote, AnalystFile, FundFile
from flask_script import Manager, prompt_bool
from openpyxl import load_workbook, Workbook
import requests
from spreadsheet import sheet
from dues import transactions, member_info


manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    admin = Role(name="Admin", description="Gets to look at all the rankings.")
    db.session.add(User(firstName="Arnav", lastName="Jain",email="arnav_jain@utexas.edu", eid="aj24872", password="test11", roles=[admin], attendance = 0, dues = 0, atLatestMeeting = False, rowOnSheet = 0, analyst = 'Srija Nalla', fund='TMT'))
    db.session.add(AnalystFile(name="WSM", filePath="https://drive.google.com/file/d/1szWz-2uHJQqWEbLJVL9RISAOfJ9k4Ja8/preview"))
    db.session.add(AnalystFile(name="DCF", filePath="https://drive.google.com/file/d/170_Gg0-e9hXgB5UMJApjsI0Y96_r4nMg/preview"))
    db.session.add(AnalystFile(name="VS", filePath="https://drive.google.com/file/d/0BwxRocCss2a5cGJ1SXBlSTBUQ0U/preview"))
    db.session.add(FundFile(name="WSM", filePath="https://drive.google.com/file/d/1szWz-2uHJQqWEbLJVL9RISAOfJ9k4Ja8/preview", fund='TMT'))
    db.session.add(FundFile(name="DCF", filePath="https://drive.google.com/file/d/170_Gg0-e9hXgB5UMJApjsI0Y96_r4nMg/preview", fund = 'TMT'))
    db.session.add(FundFile(name="VS", filePath="https://drive.google.com/file/d/0BwxRocCss2a5cGJ1SXBlSTBUQ0U/preview", fund='Energy'))
    db.session.commit()
    refreshdb()
    print 'Initialized the database'

@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print 'Dropped the database'

@manager.command
def get_attendance():
    members = User.query.filter_by(atLatestMeeting = True).all()
    count = 0

    for member in members:
        count += 1

    print("Numer of members: " + str(count))

@manager.command
def print_zero_dues():
    for user in User.query.all():
        if user.dues == 0:
            print("Name: " + user.firstName + " " + user.lastName)

@manager.command
def reset_attendance():
    eid = str(input("EID: "))
    member = User.get_by_eid(eid)
    if not member is None:
        meetings_attended = int(input("How many meetings do you want to reset it to? "))
        member.attendance = meetings_attended
        member.atLatestMeeting = False
        db.session.commit()

@manager.command
def add_dues():
    addDues = True

    while addDues:
        eid = str(raw_input("EID: "))
        member = User.get_by_eid(eid)
        if not member is None:
            dues = int(raw_input("How much dues do you want to reset it to? "))
            member.dues = dues
            db.session.commit()

        answer = raw_input("Do you want to continue (y/n)? ")
        if answer == 'y':
            addDues = True
        else:
            addDues = False

@manager.command
def get_dues():
    name_column_index = 4
    dues_column_index = 2

    trans_start_index = int(input("What row do you want to start at? "))
    trans_end_index = int(input("What row do you want to end at? "))

    transactions_unmatched = []

    for trans_index in range(trans_start_index, trans_end_index):
        fullName = str(transactions.cell(trans_index, name_column_index).value).lower()
        foundMatch = False

        for member in User.query.all():
            fullNameRecord = (member.firstName + " " + member.lastName).lower()
            if fullNameRecord == fullName:
                foundMatch = True
                if member.dues == 0:
                    dues = transactions.cell(trans_index, dues_column_index).value
                    member.dues = int(dues.split("$")[1].split(".")[0])
                    db.session.commit()
                    print("I have added", dues, "to", fullName)

        if not foundMatch:
            transactions_unmatched.append(fullName)


    print("I have not found matches for the following names: ")
    for name in transactions_unmatched:
        print(name)

@manager.command
def get_from_sheet():
    eid_column_index = 3
    firstname_column_index = 1
    lastname_column_index = 2
    email_column_index = 4
    attendance_column_index = 8

    row_index = int(input("What is the starting row? "))
    end_index = int(input("What is the ending row? "))

    for index in range(row_index, end_index):
        if str(sheet.cell(index, eid_column_index).value):
            eid = str(sheet.cell(index, eid_column_index).value).lower()
            member = User.get_by_eid(eid)
            if not member is None:
                member.firstName = str(sheet.cell(index, firstname_column_index).value).title()
                member.lastName = str(sheet.cell(index, lastname_column_index).value).title()
                member.email = str(sheet.cell(index, email_column_index).value).lower()
                # member.attendance = int(sheet.cell(index, 11).value)
                # if sheet.cell(index, 8).value:
                    # member.dues = int(sheet.cell(index, 8).value)
                # else:
                    # member.dues = 0
                # member.dues = 0
                if sheet.cell(index, attendance_column_index).value:
                    member.attendance = int(sheet.cell(index, attendance_column_index).value)
                else:
                    member.attendance = 0
                # if sheet.cell(index, 5).value:
                    # member.year = str(sheet.cell(index, 5).value)
                # else:
                    # member.year = ""
                # if sheet.cell(index, 7).value:
                    # member.comments = str(sheet.cell(index, 7).value)
                # else:
                    # member.comments = ""
                member.rowOnSheet = index
                db.session.commit()
                print("I updated the information for", member.firstName, member.lastName)
            else:
                eid = str(sheet.cell(index, eid_column_index).value).lower()
                firstName = str(sheet.cell(index, firstname_column_index).value).title()
                lastName = str(sheet.cell(index, lastname_column_index).value).title()
                email = str(sheet.cell(index, email_column_index).value).lower()
                dues = 0
                # # attendance = int(sheet.cell(index, 11).value)
                # if sheet.cell(index, 8).value:
                #   dues = int(sheet.cell(index, 8).value)
                # else:
                #   dues = 0
                if sheet.cell(index, attendance_column_index).value:
                    attendance = int(sheet.cell(index, attendance_column_index).value)
                else:
                    attendance = 0
                # if sheet.cell(index, 5).value:
                #   year = str(sheet.cell(index, 5).value)
                # else:
                #   year = ""
                # if sheet.cell(index, 7).value:
                #   comments = str(sheet.cell(index, 7).value)
                # else:
                #   comments = ""
                rowOnSheet = index
                member = Member(eid = eid, firstName = firstName, lastName = lastName, email = email, dues = dues, attendance = attendance, rowOnSheet = rowOnSheet)
                db.session.add(member)
                print("I added", firstName, lastName)
                db.session.commit()
                # print("He/she is not in the database.")
        else:
            print("There is no one on row", index)

@manager.command
def write_to_sheet():
    row_index = 2
    end_index = 1000

    new_row_start = int(input("What row do you want to start at? "))

    column = int(input("What is the column for attendance? "))

    for member in User.query.filter_by(atLatestMeeting = True):
        if member.rowOnSheet is not None and member.rowOnSheet != 0:
            print("Row: ", member.rowOnSheet)
            sheet.update_cell(member.rowOnSheet, column, "X")
            member.atLatestMeeting = False
            if not str(sheet.cell(member.rowOnSheet, 1).value):
                sheet.update_cell(member.rowOnSheet, 1, member.firstName)
            if not str(sheet.cell(member.rowOnSheet, 2).value):
                sheet.update_cell(member.rowOnSheet, 2, member.lastName)
            if not str(sheet.cell(member.rowOnSheet, 4).value):
                sheet.update_cell(member.rowOnSheet, 4, member.email)
            print("I updated attendance in column", column, "for", member.firstName, member.lastName)
            db.session.commit()
        else:
            for index in range(new_row_start, end_index):
                if not str(sheet.cell(index, 1).value) and not str(sheet.cell(index, 2).value) and not str(sheet.cell(index, 3).value):
                    print("Row: ", index)
                    sheet.update_cell(index, 1, member.firstName)
                    sheet.update_cell(index, 2, member.lastName)
                    sheet.update_cell(index, 3, member.eid)
                    sheet.update_cell(index, 4, member.email)
                    sheet.update_cell(index, column, "X")
                    member.rowOnSheet = index
                    member.atLatestMeeting = False
                    db.session.commit()
                    print("I added in the info for", member.firstName, member.lastName, "and updated attendance in column", column)
                    break;

@manager.command
def reset_vote_table():
    Vote.__table__.drop(db.session.bind)
    Vote.__table__.create(db.session.bind)

@manager.command   
def create_vote_table():
    Vote.__table__.create(db.session.bind)

@manager.command
def create_recent_vote_table():
    RecentVote.__table__.create(db.session.bind)

@manager.command
def reset_recent_vote_table():
    RecentVote.__table__.drop(db.session.bind)
    RecentVote.__table__.create(db.session.bind)

@manager.command
def count_no_names():
    count = 0
    for user in User.query.all():
        if not user.firstName or not user.lastName:
            count += 1
    print(str(count) + " people have no names in the database.")

@manager.command
def get_votes():
    ticker = str(raw_input("Ticker: ")).upper()

    numLong = Vote.query.filter_by(ticker=ticker, position="Yes - Long").count()
    numShort = Vote.query.filter_by(ticker=ticker, position="No - Short").count()
    numAbstain = Vote.query.filter_by(ticker=ticker, position="No - No Position").count()
    print("--------------- " + ticker + " Summary ---------------")
    print("Long: " + str(numLong) + ", Short: " + str(numShort) + ", Abstain: " + str(numAbstain))
    print("Number of Votes: " + str(numLong + numShort + numAbstain))

    for vote in Vote.query.filter_by(ticker=ticker):
        print("Email: " + vote.email + ", Vote: " + vote.position)

    print("--------------------------------------------")

@manager.command
def print_stocks():
    for stock in Stock.query.all():
        print(str(stock.id) + ". Stock: " + stock.ticker + ", " + str(stock.price))

    for ticker in Tickers.query.all():
        print(str(ticker.id) + ". Ticker: " + ticker.ticker + ", " + str(ticker.startingPrice) + ", " + str(ticker.short))

    for user in User.query.all():
        for stock in user.stocks:
            print(str(stock.id) + ". " + user.email + " voted for " + stock.ticker + ". Short? " + str(stock.short))
        for transaction in user.transactions:
            transTicker = Tickers.query.filter_by(ticker=transaction.ticker).first()
            if transTicker is not None:
                print(str(transaction.id) + ". " +  user.email + " took a position on " + transaction.ticker + " with return of " + str(transaction.returns/transTicker.startingPrice) + "%.")
            else:
                print(str(transaction.id) + ". " +  user.email + " took a position on " + transaction.ticker + " with return of $" + str(transaction.returns) + ".")

@manager.command
def print_returns():
    for user in User.query.all():
        print(str(user.email) + " has a return of " + str(user.ret) + "%.")

@manager.command
def delete_transactions():
    continue_or_not = 'y'

    while continue_or_not == 'y':
        id = int(input("What is the ID? "))
        transaction = Transactions.query.filter_by(id = id).first()
        db.session.delete(transaction)
        db.session.commit()
        continue_or_not = str(raw_input("Do you want to continue (y/n)? ")).lower()

@manager.command
def print_transaction_details():
    trans_id = int(input("What is the ID? "))
    transaction = Transactions.query.filter_by(id = trans_id).first()
    user = User.query.filter_by(id = transaction.user_id).first()
    print("User: " + user.email)
    print("Ticker: " + transaction.ticker)
    print("End price: " + str(transaction.end_price))
    print("Return: " + str(transaction.returns))

@manager.command
def refreshdb():
        # Refresh the stored information for each stock
    for stock in Tickers.query.all():
        create_stock_info(stock)
    # for stock in Transactions.query.all():
    #     create_stock_info(stock)
        
    # Refresh the score and ranks for each student
    for student in User.query.all():
        numStocks = update_ret(student, student.stocks, student.transactions)
        update_score(student, student.ret, numStocks)

@manager.command
def get_user_emails():
    for user in User.query.all():
        print(user.email)

@manager.command
def add_analyst_group():
    eid_input = str(input("What is the GM's EID? "))
    student = User.query.filter_by(eid = eid_input)
    if student is not None:
        fullName = student.firstName + " " + student.lastName
        analyst_group = str(input("Please list the senior analyst for {}".format(fullName)))
        student.analyst = analyst_group
        db.session.commit()

    student_new = User.query.filter_by(eid = eid_input)
    fullName = student.firstName + " " + student.lastName
    print(student_new + " is {}'s SA.".format(fullName))

@manager.command
def addstock():
    name = str(raw_input("What is the file name? "))
    symbol = str(raw_input("Ticker: "))
    price = int(raw_input("Starting price: $"))
    num_votes = int(raw_input("How many votes were there? "))

    wb = load_workbook(filename=name)
    ws = wb.active

    for index in range(1, num_votes + 1):
        if str(ws['B' + str(index)].value) == 'Long':
            if  Tickers.query.filter_by(short = False, ticker = symbol).count() > 0:
                stock = Tickers.query.filter_by(short = False, ticker = symbol).first()
                print("I FOUND THE STOCK ALREADY")
            else:
                stock = Tickers(ticker=symbol, startingPrice=price, short=False)
        elif str(ws['B' + str(index)].value) == 'Short':
            if Tickers.query.filter_by(short = True, ticker = symbol).count() > 0:
                stock = Tickers.query.filter_by(short = True, ticker = symbol).first()
                print("I FOUND THE STOCK ALREADY")
            else:
                stock = Tickers(ticker=symbol, startingPrice=price, short=True)
        if User.query.filter_by(email=str(ws['A'+str(index)].value).lower()) != None:
            student = User.query.filter_by(email=str(ws['A'+str(index)].value)).first()
            add_stock(student, stock)

@manager.command
def fixdb():
    num_students = User.query.count()
    num_students_wo_id = 1
    for student in User.query.all():
        if student.id == None:
            student.id == num_students + num_students_wo_id
            num_students_wo_id += 1
            print("I fixed", student.firstName, "!")

        db.session.commit()

if __name__ == '__main__':
    manager.run()


