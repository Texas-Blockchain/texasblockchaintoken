from web3 import Web3, HTTPProvider
from exchange import uniswap_abi

# Connect to an Infura node (for now...)
w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/4e529bfe5adb43d49db599afcf381cd3"))

# Get token contract address and creator's keys
factory_address = w3.toChecksumAddress('0x9c83dCE8CA20E9aAF9D3efc003b2ea62aBC08351')
public_key = w3.toChecksumAddress('0xCbcFfBecdB81698DDF3504d4E7dbeD8565f02715')
private_key = 'CDF28FC7FDCDA6126BE2ECE17CD2008F7C4FB77F25E07F5D810F933BA72E0FA2'

factory_contract = w3.eth.contract(address=factory_address, abi=uniswap_abi.abi)

print(factory_contract.all_functions())

tx_count = w3.eth.getTransactionCount(public_key)

create_exchange_tx = factory_contract.functions.createExchange(w3.toChecksumAddress('0x35cae81ed8ed242e7db6edcafeab04a91cd60184'))
print(create_exchange_tx)

tx = create_exchange_tx.buildTransaction({'gas': 1000000, 'nonce': tx_count})
print(tx)

signed = w3.eth.account.signTransaction(tx, private_key)

txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
success = w3.eth.waitForTransactionReceipt(txn_hash)
print(success)

# Add liquidity
liquidity_tx = factory_contract.functions.addLiquidity