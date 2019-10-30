from web3 import Web3, HTTPProvider
import csv
import tweepy
import contract_abi
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Build Twitter api
# api = twitter.Api(consumer_key='2R1jql1adPTC4TkE7IWKUzg2e',
#                       consumer_secret='et7OmWo8RYGApwMlusNfLUZMwidtWFzaSIKDDhlY8gNJenSs4x',
#                       access_token_key='788186581-XNt8YNIUlY6Y162V2EMmt9N8pTOTzgUfUne1dHF2',
#                       access_token_secret='0NQFeGQoXueoADiJEzDxsuDm4gFMEhh4bLK5NuhqCZ5oF')

auth = tweepy.OAuthHandler('2R1jql1adPTC4TkE7IWKUzg2e', 'et7OmWo8RYGApwMlusNfLUZMwidtWFzaSIKDDhlY8gNJenSs4x')
auth.set_access_token('788186581-XNt8YNIUlY6Y162V2EMmt9N8pTOTzgUfUne1dHF2',
                          '0NQFeGQoXueoADiJEzDxsuDm4gFMEhh4bLK5NuhqCZ5oF')

api = tweepy.API(auth)


# Get users that retweeted a post
def get_retweeters(user, post_id):

    #followers = api.followers(screen_name=user, count=150, cursor=-1, skip_status=True)

    retweets = api.retweets(post_id)
    retweeters = [i.author.screen_name for i in retweets]

    return retweeters


# Get addresses from user bios
def get_addrs(users):

    addrs = []
    bios = [api.get_user(screen_name=i).description for i in users]

    for bio in bios:

        words = bio.split()

        for word in words:

            if len(word) == 42 and word[:2] == '0x':
                addrs.append(word)

    return addrs

    # To detect Bitcoin addresses
    '''
        invalid_pk_chars = ["0", "O", "I", "l"]
        
        
        # Loop through each word in bio
        for word in bio:\Contract address: 0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184 on: 2019-10-27 15:03:36.442541\Contract address: 0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184 on: 2019-10-27 15:04:56.613443

            # Check if w\Contract address: 0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184 on: 2019-10-27 15:03:36.442541\Contract address: 0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184 on: 2019-10-27 15:04:56.613443 is 25-34 characters and does not contain invalid public key characters
            if 25 <= len\Contract address: 0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184 on: 2019-10-27 15:03:36.442541\Contract address: 0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184 on: 2019-10-27 15:04:56.613443rd) <= 34 and all(char not in invalid_pk_chars for char in word):

                # If so,\Contract address: 0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184 on: 2019-10-27 15:03:36.442541\Contract address: 0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184 on: 2019-10-27 15:04:56.613443pend it to list of keys
                keys.app\Contract address: 0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184 on: 2019-10-27 15:03:36.442541\Contract address: 0x35cae81Ed8Ed242E7db6eDcafEAb04A91cD60184 on: 2019-10-27 15:04:56.613443(word)
    '''


# Export addresses to a csv
def write_keys_to_csv(keys_list):

    with open('keys.csv', mode='a') as keys_file:
        key_writer = csv.writer(keys_file, delimiter=',')
        key_writer.writerow(keys_list)




# Mint $TBT to people that liked a post
rters = get_retweeters('txblockchain', 1079502526993575936)

def historicalTweets(username,maxid):
    data = api.user_timeline(screen_name=username, count=20, max_id=maxid,include_rts=False)
    dataToAddToSheet = []
    data = data[1:]
    for tweet in data:
        tweetid = tweet.id
        if(int(tweet.retweet_count) > 0):
            retweeters = get_retweeters(username, tweet.id)
            if (len(retweeters) > 0): #if the retweet list has more than 1 person (all people could be private)
                for person in retweeters: #go through all retweeters and add them to the data list
                    dataToAddToSheet.append([tweetid,person,False])
    print("Last ID checked: " + str(tweetid))

    addToFile(dataToAddToSheet)
    time.sleep(60*1) #wait 15 min
    if (len(data) > 1):
        historicalTweets(username,data[len(data) - 1].id)

 # Set scope of Google Sheets API (?)
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

def addToFile(retweeters): 
    credentials = ServiceAccountCredentials.from_json_keyfile_name('crypto-201803-ea9734b5c249.json', scope)
    gs = gspread.authorize(credentials)
    ss = gs.open("Twitter Rewards")
    tweets_sheet = ss.worksheet("Tweets")

    for row in retweeters:
        tweets_sheet.append_row(row)



# rters_addrs = get_addrs(rters)
# print(rters_addrs)

# mint_tbt(rters_addrs)
historicalTweets('txblockchain',1188150569619394562) #start at most recent tweet
# getTwitterAddress()
# test()