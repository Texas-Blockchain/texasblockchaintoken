from web3 import Web3, HTTPProvider
import csv
import tweepy
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Build Twitter api

auth = tweepy.OAuthHandler('I5b7mStfc3AiXi8CUlZVzOwyE', 'nlC6jN3JI3EBFsgYwEP0jBLHIe6vs5mQa241bGbTYkf5v7qfTm')
auth.set_access_token('942938133032816640-qni5kCujzzaQkz5U480BwhB8yZL1n2U',
                          'iHUsNv4mELA54tMQSpuUC9tfTOw7Kj3b0TMqZhFPL56ce')

api = tweepy.API(auth)
 # Set scope of Google Sheets API (?)
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']


# Get users that retweeted a certain post
def get_retweeters(post_id):
    retweets = api.retweets(post_id)
    retweeters = [i.author.screen_name for i in retweets]

    return retweeters


#go through all historical tweets and add them to the master list so those users can be given tbt
def historical_tweets(username,maxid):
    data = api.user_timeline(screen_name=username, count=20, max_id=maxid,include_rts=False)
    sheet_data = []
    data = data[1:]
    for tweet in data:
        tweetid = tweet.id
        if(int(tweet.retweet_count) > 0):
            retweeters = get_retweeters(tweet.id)
            if (len(retweeters) > 0): #if the retweet list has more than 1 person (all people could be private)
                for person in retweeters: #go through all retweeters and add them to the data list
                    sheet_data.append([tweetid,person,False])
    print("Last ID checked: " + str(tweetid))

    add_to_file(sheet_data)
    time.sleep(60*1) #wait 15 min
    if (len(data) > 1):
        historical_tweets(username,data[len(data) - 1].id)


#add a list of retweeters to the twitter participants sheet
def add_to_file(retweeters): 
    credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
    gs = gspread.authorize(credentials)
    ss = gs.open("Twitter Rewards")
    tweets_sheet = ss.worksheet("Tweets")

    for row in retweeters:
        tweets_sheet.append_row(row)


#check direct messages and update spreadsheet
def check_direct_messages():
    messages = api.list_direct_messages()
    participants  = get_partipants_from_sheet()
    messages = messages[::-1] #reverse the list so its from reverse chronologically so newer messages replace old ones
    #go through all DMs
    for i in range(len(messages)):
        message = messages[i]
        data = message.message_create
        #first check if the tweet contains an eth address
        text = data['message_data']['text']
        if text[:2] == '0x':
            #check if the address is already in the sheet. 
            #Useful so users can't have multiple addresses and to avoid extra calls to Twitter API
            address_exists = False
            for person in participants:
                if text[:42] in person:
                    address_exists = True
                    break
            if not address_exists and len(text) == 42:
                update_sheet_with_address(data,participants,text)
              
#Update the spreadsheet to add or edit a twitter user's address
def update_sheet_with_address(data, participants,text):
    #get their twitter handle 
    screen_name = (api.get_user(data['sender_id']))
    screen_name = screen_name._json['screen_name']
    #go through all rows of spreadsheet and see if their handle is already there
    row_number = 1
    user_on_sheet = False
    for person in participants:
        if screen_name in person:
            #found the user's data on the sheet, let's update it with their address
            print(f"Updating sheet at B{row_number}")
            update_sheet(row_number, text)
            user_on_sheet = True
            break
        row_number += 1
    if not user_on_sheet:
        print(f"Adding a new row")
        add_user_to_sheet(screen_name,text,row_number)

#Return a list of lists of all people in sheet.
#List elements: ['Name', 'Address', 'Email', 'Twitter']
#Example: people[1][0] will return the name of the first person. people[1][1] will return their TBT address
def get_partipants_from_sheet():
    credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
    gs = gspread.authorize(credentials)
    ss = gs.open("Master Spreadsheet")
    sheet = ss.worksheet("Participants")
    people = sheet.get_all_values()
    return people    

#update the sheet with the eth address w/ a certain twitter handle
def update_sheet(rowNumber, address):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
    gs = gspread.authorize(credentials)
    ss = gs.open("Master Spreadsheet")
    sheet = ss.worksheet("Participants")
    address = address[:42]
    return sheet.update_cell(rowNumber,2,address)

#add a new user to the end of the sheet
#called when a DM is recieved but the twitter handle wasn't already on the sheet
def add_user_to_sheet(handle, address, rowNumber):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
    gs = gspread.authorize(credentials)
    ss = gs.open("Master Spreadsheet")
    sheet = ss.worksheet("Participants")
    address = address[:42]
    sheet.update_cell(rowNumber,2,address)
    return sheet.update_cell(rowNumber,4,handle)

# check_direct_messages()