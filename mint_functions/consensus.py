from web3 import Web3, HTTPProvider
import csv
import tweepy
import contract_abi
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
gs = gspread.authorize(credentials)
ss = gs.open("Consensus Form (Responses)")
sheet = ss.worksheet("Responses")

