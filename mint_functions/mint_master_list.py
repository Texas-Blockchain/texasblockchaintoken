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
    sheet = ss.worksheet("Tweets")
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
        if handle in participants.keys() and paid_out == 'FALSE':
            address = participants[handle]
            payout_list.append([address, cell_number])
        cell_number += 1
    mint_tbt(payout_list)

#Mint $TBT to a list of addresses
#Recieves a list of lists containing [tbt address,row number]
#After minting, update the cell address to TRUE
def mint_tbt(addresses):
    # Connect to an Ethereum node using Infura
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

    # Get contract address and owner's keys
    contract_address = w3.toChecksumAddress('0x35cae81ed8ed242e7db6edcafeab04a91cd60184')
    public_key = w3.toChecksumAddress('0xCbcFfBecdB81698DDF3504d4E7dbeD8565f02715')
    private_key = 'CDF28FC7FDCDA6126BE2ECE17CD2008F7C4FB77F25E07F5D810F933BA72E0FA2'
    #TODO: CORRECT DIR NAME
    dirname = "/home/bitcoinnode/texasblockchaintoken/mint_functions"

    # Get contract object using web3
    contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)

    txn_hashes = []

    # Loop through list of addresses (passed as an argument)
    for address in addresses:
        tbt_address = address[0]
        cell = address[1]
        # Get transaction count of address to use as nonce for next transaction
        tx_count = w3.eth.getTransactionCount(public_key)

        # Build transaction
        mint_tx = contract.functions.mint(tbt_address, 10000000000000000000).buildTransaction({'gas': 1000000, 'nonce': tx_count})

        # Sign transaction
        signed = w3.eth.account.signTransaction(mint_tx, private_key)

        # Submit transaction
        txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        txn_hashes.append(txn_hash.hex())

        #Mark as paid on sheet
        update_sheet(cell)

    print(txn_hashes)


#Mark tweet as paid
def update_sheet(rowNumber):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
    gs = gspread.authorize(credentials)
    ss = gs.open("Master Spreadsheet")
    sheet = ss.worksheet("Tweets")
    return sheet.update_cell(rowNumber,3,'TRUE')

# payout_retweeters()
