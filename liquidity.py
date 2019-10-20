from web3 import Web3, HTTPProvider
import contract_abi

# Connect to an Infura node
w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

# Get token contract address and creator's keys
token_address = w3.toChecksumAddress('0x35cae81ed8ed242e7db6edcafeab04a91cd60184')
exchange_address = w3.toChecksumAddress('0xB7172917860e1ca84913C300b366aD11C0d1305c')
public_key = w3.toChecksumAddress('0xCbcFfBecdB81698DDF3504d4E7dbeD8565f02715')
private_key = 'CDF28FC7FDCDA6126BE2ECE17CD2008F7C4FB77F25E07F5D810F933BA72E0FA2'

token_contract = w3.eth.contract(address=token_address, abi=contract_abi.abi)

tx_count = w3.eth.getTransactionCount(public_key)

print(token_contract.all_functions())

approve_tx = token_contract.functions.approve(exchange_address, 1000)

tx = approve_tx.buildTransaction({'gas': 1000000, 'nonce': tx_count})
print(tx)

signed = w3.eth.account.signTransaction(tx, private_key)

txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
success = w3.eth.waitForTransactionReceipt(txn_hash)
print(success)