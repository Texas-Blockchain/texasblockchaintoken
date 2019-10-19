import pyqrcode
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from web3 import Web3, HTTPProvider, gas_strategies
import contract_abi
import time
from PIL import Image
import numpy as np
import png

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
time.sleep(30)

# MINT TOKENS TO ATTENDEES
# Set scope of Google Sheets API (?)
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Get instance of Google Sheets API using credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
gs = gspread.authorize(credentials)

# Get attendance sheet from QR code form
sheet = gs.open("Proof of Attendance TEST (Responses)").sheet1

# Get attendees
attendees = sheet.col_values(2)[1:]

# Connect to an Infura node (for now...)
w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

# Get token contract address and creator's keys
contract_address = w3.toChecksumAddress('0x35cae81ed8ed242e7db6edcafeab04a91cd60184')
public_key = w3.toChecksumAddress('0xCbcFfBecdB81698DDF3504d4E7dbeD8565f02715')
private_key = 'CDF28FC7FDCDA6126BE2ECE17CD2008F7C4FB77F25E07F5D810F933BA72E0FA2'

# Get contract object using web3
contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)

attendees = [x for x in attendees if x != '']
attendees = np.unique(attendees)

# Get transaction count of address to use as nonce for next transaction


# Loop through list of addresses (passed as an argument)
for pk in attendees:

    tx_count = w3.eth.getTransactionCount(public_key)
    print(pk)
    # Build transaction
    mint_tx = contract.functions.mint(pk, 10000000000000000000)
    print(w3.eth.gasPrice)
    print(mint_tx)
    #print(mint_tx.estimateGas())
    tx = mint_tx.buildTransaction({'gas': 1000000, 'nonce': tx_count})
    print(tx)

    # Sign transaction
    signed = w3.eth.account.signTransaction(tx, private_key)

    # Send transaction
    txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    success = w3.eth.waitForTransactionReceipt(txn_hash)
    print(success)

    tx_count += 1