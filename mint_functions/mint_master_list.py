from web3 import Web3, HTTPProvider
import csv
import contract_abi
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']


#Returns a dictionary of users as {handle:address}
def map_of_users():
    credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
    gs = gspread.authorize(credentials)
    ss = gs.open("Master Spreadsheet")
    sheet = ss.worksheet("Participants")
    people = sheet.get_all_values()
    proper_users = {}
    for person in people:
        address = person[1]
        if (len(address) == 42):
            handle = person[3]
            proper_users[handle] = address
    return proper_users

#Return a list of lists of all people in sheet.
#List elements: ['Name', 'Address', 'Email', 'Twitter']
#Example: people[1][0] will return the name of the first person. people[1][1] will return their TBT address
def list_of_tweets():
    credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
    gs = gspread.authorize(credentials)
    ss = gs.open("Master Spreadsheet")
    sheet = ss.worksheet("Payouts")
    return sheet.get_all_values()

 #Go through all tweets in sheet and if we have their tbt address and they haven't been paid for that tweet, mint           
def payout_retweeters(): 
    participants = map_of_users()
    tweets = list_of_tweets()
    payout_list = []
    cell_number = 1

    #go through list of tweets that need to be paid out and add to a list
    for tweet in tweets:
        handle = tweet[1]
        paid_out = tweet[2]
        amount = tweet[3]
        tbt_address = tweet[4]

        if handle in participants.keys() and paid_out == 'FALSE':
            address = participants[handle]
            payout_list.append([address, cell_number, amount])
        elif len(tbt_address) == 42 and paid_out == 'FALSE':
            payout_list.append([tbt_address, cell_number, amount])
        cell_number += 1
    if len(payout_list) > 0:
        mint_tbt(payout_list)

#Mint $TBT to a list of addresses
#Recieves a list of lists containing [tbt address,row number]
#After minting, update the cell address to TRUE
real_contract = '0x9e2b0752131CB2F424f39Ce509CccB230Cd9304f'
real_public_key = '0x6D10875b3C3F53F1C1cf9aE130B1A415790f8Cf3'
real_private_key = '74BC2E012071FCA65CA31FA7AFE0483929A451180ACBF9D9647A06AC30E69957'
def mint_tbt(addresses):
    print("Paying out to:")
    print(str(addresses))
    # Connect to an Ethereum node using Infura
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

    # Get contract address and owner's keys
    contract_address = w3.toChecksumAddress('0x9e2b0752131CB2F424f39Ce509CccB230Cd9304f')
    public_key = w3.toChecksumAddress('0x6D10875b3C3F53F1C1cf9aE130B1A415790f8Cf3')
    private_key = '74BC2E012071FCA65CA31FA7AFE0483929A451180ACBF9D9647A06AC30E69957'
    #TODO: CORRECT DIR NAME
    dirname = "/Users/jacksharkey/Documents/texasblockchain/tbt/mint_functions"

    # Get contract object using web3
    contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)

    txn_hashes = []

    # Loop through list of addresses (passed as an argument)
    for address in addresses:
        tbt_address = address[0]
        cell = address[1]
        amount = address[2]
        tbt_address = w3.toChecksumAddress(tbt_address)
        # Get transaction count of address to use as nonce for next transaction
        tx_count = w3.eth.getTransactionCount(public_key)
        wei_amount = w3.toWei(amount, 'ether')
        # Build transaction
        mint_tx = contract.functions.mint(tbt_address, wei_amount).buildTransaction({'gas': 1000000, 'nonce': tx_count})
        # Sign transaction
        signed = w3.eth.account.signTransaction(mint_tx, private_key)

        # Submit transaction
        txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        success = w3.eth.waitForTransactionReceipt(txn_hash)
        txn_hashes.append(txn_hash.hex())
        print("Mint successful.")

        #Mark as paid on sheet
        update_sheet(cell)
        # time.sleep(3)

    # print(txn_hashes)


#Mark tweet as paid
def update_sheet(rowNumber):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
    gs = gspread.authorize(credentials)
    ss = gs.open("Master Spreadsheet")
    sheet = ss.worksheet("Payouts")
    return sheet.update_cell(rowNumber,3,'TRUE')

while(1):
    print("Checking")
    payout_retweeters()
    time.sleep(60)
