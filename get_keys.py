import requests
from bs4 import BeautifulSoup
import csv
from web3 import Web3, HTTPProvider

# Gets the 9 most recent user-ids that liked a post
def get_users_that_liked_post(post_id):

    # Create list for users
    user_list = []

    # Get tweet from parameter post_id
    url = 'https://twitter.com/lawrencehwhite1/status/' + str(post_id)
    response = requests.get(url)
    page = BeautifulSoup(response.content, 'lxml')

    # Get all recent likers of tweet
    tweet_likers = page.find_all('a', {'class': 'js-profile-popup-actionable'})

    # Append each liker to users list
    for i in tweet_likers:
        try:
            user_list.append(i.attrs['href'][1:])
        except:
           user_list.append('NA')

    return user_list

def get_keys_from_user_bios(user_list):

    keys = []

    for user in user_list:

        url = 'https://twitter.com/' + str(user)
        response = requests.get(url)
        page = BeautifulSoup(response.content, 'lxml')

        bio = page.find('p', {'class': 'ProfileHeaderCard-bio'}).text.strip()

        bio_list = bio.split()

        invalid_pk_chars = ["0", "O", "I", "l"]

        # Loop through each word in bio
        for word in bio_list:

            # Check if word is 25-34 characters and does not contain invalid public key characters
            if 25 <= len(word) <= 34 and all(char not in invalid_pk_chars for char in word):

                # If so, append it to list of keys
                keys.append(word)

    return keys

def write_keys_to_csv(keys_list):

    with open('keys.csv', mode='a') as keys_file:
        key_writer = csv.writer(keys_file, delimiter=',')
        key_writer.writerow(keys_list)


