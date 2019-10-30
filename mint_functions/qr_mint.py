import pyqrcode
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from web3 import Web3, HTTPProvider
import contract_abi
import time
from PIL import Image
import numpy as np

# Set link to attendance form
attendance_form = "https://docs.google.com/forms/d/e/1FAIpQLSdnL6EBvtLuDfDzMdvM76b7CJnSHHRtDOKBvTy3tioEzZkERw/viewform?usp=sf_link"

# Create QR code
url = pyqrcode.create(attendance_form)
print(url)

# Get current date
timestamp = str(time.strftime("%x %X", time.gmtime()))[:8]
timestamp = timestamp.replace('/', '_')
print(timestamp)

file_name = 'attendance_' + timestamp + '.png'
print(file_name)

# Create and save QR code file
url.png(file_name, scale=8)

# Show QR code
img = Image.open(file_name)
img.show()

# Start countdown to mint
time.sleep(0)

# Mint tokens to attendees

# Set scope of Google Sheets API (?)
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Get instance of Google Sheets API using credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
gs = gspread.authorize(credentials)

# Get attendance sheet from QR code form
ss = gs.open("Proof of Attendance TEST (Responses)")
sheet_list = ss.worksheets()

try:
    sheet = ss.add_worksheet(title='attendance_' + timestamp, rows=100, cols=2)
except:
    sheet = ss.worksheet('attendance_' + timestamp)

print(ss.worksheets())

# Get attendees
attendees = sheet.col_values(2)[1:]
print(attendees)
# Connect to an Ethereum node using Infura
w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

# Get token contract address and creator's keys
contract_address = w3.toChecksumAddress('0x9e2b0752131cb2f424f39ce509cccb230cd9304f')
public_key = w3.toChecksumAddress('0x6D10875b3C3F53F1C1cf9aE130B1A415790f8Cf3')
private_key = '74BC2E012071FCA65CA31FA7AFE0483929A451180ACBF9D9647A06AC30E69957'

# Get contract object using web3
contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)

attendees = [x for x in attendees if x != '']
attendees = np.unique(attendees)

print(attendees)
# Loop through list of addresses (passed as an argument)
for pk in attendees:

    # Get transaction count of minter address to use as nonce for next transaction
    tx_count = w3.eth.getTransactionCount(public_key)

    # Build transaction
    mint_tx = contract.functions.burn(pk, 225000000000000000000)
    print(mint_tx)

    tx = mint_tx.buildTransaction({'gas': 1000000, 'nonce': tx_count})
    print(tx)

    # Sign transaction
    signed = w3.eth.account.signTransaction(tx, private_key)


    # Send transaction
    txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    success = w3.eth.waitForTransactionReceipt(txn_hash)
    print(success)

    # Send transaction
    txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    success = w3.eth.waitForTransactionReceipt(txn_hash)
    print(success)

