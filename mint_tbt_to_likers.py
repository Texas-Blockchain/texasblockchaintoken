from web3 import Web3, HTTPProvider
import contract_abi
import get_keys

# --Takes a list of addresses and mints $TBT to each one--

def mint_tbt_to_likers(addresses):

    # Connect to an Infura node (for now...)
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

    # Get token contract address and creator's keys
    contract_address = w3.toChecksumAddress('0x35cae81ed8ed242e7db6edcafeab04a91cd60184')
    public_key = w3.toChecksumAddress('0xCbcFfBecdB81698DDF3504d4E7dbeD8565f02715')
    private_key = 'CDF28FC7FDCDA6126BE2ECE17CD2008F7C4FB77F25E07F5D810F933BA72E0FA2'

    # Get contract object using web3
    contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)
    print(contract.all_functions())

    # Loop through list of addresses (passed as an argument)
    for key in addresses:

        # Get transaction count of address to use as nonce for next transaction
        tx_count = w3.eth.getTransactionCount(public_key)

        # Build transaction
        mint_tx = contract.functions.mint(key, 10000000000000000000).buildTransaction({'gas': 1000000, 'nonce': tx_count})

        # Sign transaction
        signed = w3.eth.account.signTransaction(mint_tx, private_key)

        # Send transaction
        txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        print(txn_hash)

# Get list of users that liked a post
likers = get_keys.get_users_that_liked_post(1137804453338386432)

# Get the Ethereum address from each user's bio (if there is one)
likers_keys = get_keys.get_keys_from_user_bios(likers)
print(likers_keys)

# Mint and distribute $TBT to these each liker's address
mint_tbt_to_likers(likers_keys)

# Write the keys to a file (to be built into a kind of Leaderboard)
get_keys.write_keys_to_csv(likers_keys)

