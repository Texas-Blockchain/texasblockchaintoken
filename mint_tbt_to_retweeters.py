from web3 import Web3, HTTPProvider
import csv
import twitter
import tweepy
import contract_abi

# Build Twitter api
api = twitter.Api(consumer_key='2R1jql1adPTC4TkE7IWKUzg2e',
                      consumer_secret='et7OmWo8RYGApwMlusNfLUZMwidtWFzaSIKDDhlY8gNJenSs4x',
                      access_token_key='788186581-XNt8YNIUlY6Y162V2EMmt9N8pTOTzgUfUne1dHF2',
                      access_token_secret='0NQFeGQoXueoADiJEzDxsuDm4gFMEhh4bLK5NuhqCZ5oF')

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
        for word in bio:

            # Check if word is 25-34 characters and does not contain invalid public key characters
            if 25 <= len(word) <= 34 and all(char not in invalid_pk_chars for char in word):

                # If so, append it to list of keys
                keys.append(word)
    '''


# Export addresses to a csv
def write_keys_to_csv(keys_list):

    with open('keys.csv', mode='a') as keys_file:
        key_writer = csv.writer(keys_file, delimiter=',')
        key_writer.writerow(keys_list)


# Mint $TBT to a list of addresses
def mint_tbt(addresses):

    # Connect to an Ethereum node using Infura
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

    # Get contract address and owner's keys
    contract_address = w3.toChecksumAddress('0x35cae81ed8ed242e7db6edcafeab04a91cd60184')
    public_key = w3.toChecksumAddress('0xCbcFfBecdB81698DDF3504d4E7dbeD8565f02715')
    private_key = 'CDF28FC7FDCDA6126BE2ECE17CD2008F7C4FB77F25E07F5D810F933BA72E0FA2'

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

# Mint $TBT to people that liked a post
rters = get_retweeters('txblockchain', 1079502526993575936)
rters_addrs = get_addrs(rters)
print(rters_addrs)
mint_tbt(rters_addrs)