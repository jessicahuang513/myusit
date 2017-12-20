import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

transactions = client.open("USIT Membership Reports 2017-2018").get_worksheet(1)
member_info = client.open("USIT Membership Reports 2017-2018").get_worksheet(0)