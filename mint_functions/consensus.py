import pandas as pd
from web3 import Web3, HTTPProvider
import csv
import tweepy
import contract_abi
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import numpy as np

# Set scope of Google Sheets API (?)
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
gs = gspread.authorize(credentials)
ss = gs.open("Master Sheet")
sheet = ss.worksheet("Consensus")

responses = sheet.get_all_values()
headers = responses.pop(0)

df = pd.DataFrame(responses, columns=headers)

w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

# Get token contract address and creator's keys
contract_address = w3.toChecksumAddress('0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184')
public_key = w3.toChecksumAddress('0xCbcFfBecdB81698DDF3504d4E7dbeD8565f02715')
private_key = 'CDF28FC7FDCDA6126BE2ECE17CD2008F7C4FB77F25E07F5D810F933BA72E0FA2'

# Get contract object using web3
contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)

# Loop through list of addresses (passed as an argument)
for pk, peer in zip(np.unique(df['Ethereum Address']), df['Peer - "Firstname Lastname"']):

    sheet = ss.worksheet("Participants")

    responses = sheet.get_all_values()
    headers = responses.pop(0)

    df = pd.DataFrame(responses, columns=headers)

    pks = sheet.col_values(1)
    peer_pk = [i[0] for i in zip(df['Address'], df['Name']) if i[1] == peer]

    # Get transaction count of minter address to use as nonce for next transaction
    tx_count = w3.eth.getTransactionCount(public_key)

    # Build transaction
    mint_tx = contract.functions.burn(pk, 2000000000000000000)
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
