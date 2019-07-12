from web3 import Web3, HTTPProvider
import contract_abi
import get_keys

# --Takes a list of addresses and mints $TBT to each one--

def mint_tbt_to_likers(addresses):

    # Connect to an Infura node (for now...)
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

    # Get token contract address and creator's keys
    contract_address = w3.toChecksumAddress('0x914f14a9fff4ab5ef6c421b36574e97f2979ad9d')
    public_key = w3.toChecksumAddress('0xCbcFfBecdB81698DDF3504d4E7dbeD8565f02715')
    private_key = 'CDF28FC7FDCDA6126BE2ECE17CD2008F7C4FB77F25E07F5D810F933BA72E0FA2'

    # Unlock creator's account?
    w3.personal.unlockAccount(public_key, private_key)

    # Get contract object using web3
    contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)

    # Loop through list of addresses (passed as an argument)
    for key in addresses:

        # BUILT TRANSACTION ???
        #mint_tx = contract.functions.mint(1).buildTransaction({'from': w3.toChecksumAddress('0x914f14a9fff4ab5ef6c421b36574e97f2979ad9d')})

        # MINT ???
        mint_tx = contract.functions.mint(1)
        #mint_tx.estimateGas()
        contract.functions.mint(1).transact({'gas': '1000000000000000000'})
        print(mint_tx)

        # TRANSFER TO ADDRESS
        transaction = contract.functions.transfer(key, 1).transact({'gas': 60000000000})

# Get list of users that liked a post
likers = get_keys.get_users_that_liked_post(1137804453338386432)

# Get the Ethereum address from each user's bio (if there is one)
likers_keys = get_keys.get_keys_from_user_bios(likers)
print(likers_keys)

# Mint and distribute $TBT to these each liker's address
mint_tbt_to_likers(likers_keys)

# Write the keys to a file (to be built into a kind of Leaderboard)
get_keys.write_keys_to_csv(likers_keys)

