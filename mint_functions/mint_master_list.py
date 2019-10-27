from web3 import Web3, HTTPProvider
import csv
import contract_abi
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']


def payoutRetweeters(retweeters): 
    # Get attendance sheet from QR code form
    # Get instance of Google Sheets API using credentials
    credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
    gs = gspread.authorize(credentials)
    # retweeters = retweeters[0]
 
    ss = gs.open("Twitter Rewards")
    sheet_list = ss.worksheets()

    participant_sheet = ss["Participants"]
    tweets_sheet = ss["Tweets"]
    screen_names = participant_sheet.col_values(1)[1:]
    addresses = participant_sheet.col_values(2)[1:]
    participants = {}


    #make a dictionary of all people in sheet
    for x,y in zip(screen_names,addresses):
        participants[x] = y

    # print(participants)

    payout_list = []
    #go through list of retweeters
    for person in retweeters:
        print("person" + str(person))
        print(participants.keys())
        if (person in list(participants.keys())):
            print("person is in the list")
            print(participants[person]) #print their address
            payout_list.append(participants[person])
            #pay them out b/c we have their address

    print(payout_list)
    if (len(payout_list) > 0):
        mint_tbt(payout_list)

# Mint $TBT to a list of addresses
def mint_tbt(addresses):

    # Connect to an Ethereum node using Infura
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

    # Get contract address and owner's keys
    contract_address = w3.toChecksumAddress('0x35cae81ed8ed242e7db6edcafeab04a91cd60184')
    public_key = w3.toChecksumAddress('0xCbcFfBecdB81698DDF3504d4E7dbeD8565f02715')
    private_key = 'CDF28FC7FDCDA6126BE2ECE17CD2008F7C4FB77F25E07F5D810F933BA72E0FA2'
    dirname = "/home/bitcoinnode/texasblockchaintoken/mint_functions"
    myFile = open(dirname + '/retweetchecks.txt', 'a') 
    myFile.write('\Contract address: ' + str(contract_address) + ' on: ' + str(datetime.now()) + '\n')

    # Get contract object using web3
    contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)
    print(contract.all_functions())

    txn_hashes = []

    # Loop through list of addresses (passed as an argument)
    for addr in addresses:

        # Get transaction count of address to use as nonce for next transaction
        tx_count = w3.eth.getTransactionCount(public_key)

        # Build transaction
        mint_tx = contract.functions.mint(addr, 10000000000000000000).buildTransaction({'gas': 1000000, 'nonce': tx_count})

        # Sign transaction
        signed = w3.eth.account.signTransaction(mint_tx, private_key)

        # Submit transaction
        txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        txn_hashes.append(txn_hash.hex())

    print(txn_hashes)
