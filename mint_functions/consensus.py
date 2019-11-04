from web3 import Web3, HTTPProvider
import csv
import tweepy
import contract_abi
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Set scope of Google Sheets API (?)
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
gs = gspread.authorize(credentials)
ss = gs.open("Consensus Form (Responses)")
sheet = ss.worksheet("Responses")

email = sheet.col_values(1)[1:]
peer_email = sheet.col_values(2)[1:]
date = sheet.col_values(3)[1:]
execution = sheet.col_values(4)[1:]
creativity = sheet.col_values(5)[1:]
practicality = sheet.col_values(6)[1:]
respect = sheet.col_values(7)[1:]

