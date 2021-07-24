'''
accounts
get balance
send transaction
call
transact
deploy
'''

# setup
from web3 import Web3, HTTPProvider

from pprint import pprint
import json

TRUFFLE = 'YOUR API KEY'
url = 'https://sandbox.truffleteams.com/' + TRUFFLE
web3 = Web3(HTTPProvider(url))

# accounts
accounts = web3.eth.accounts
pprint(accounts)

# get balance
bal = web3.eth.get_balance('0x61eB15d8A761Fc80387F50d84Fbf7Ff47a97d92F')
print(bal)

bals = [
    web3.eth.get_balance(account)
    for account in accounts
]
pprint(bals)

# send transaction
user, charity, store = accounts[:3]
web3.eth.defaultAccount = user
hash = web3.eth.sendTransaction(
    {
        'to': charity,
        'value': 0,
    }
)
pprint(hash)

# call
with open('contract/abi.json') as f:
    abi = json.load(f)
with open('contract/address.txt') as f:
    address = f.read()

contract = web3.eth.contract(address=address, abi=abi)
asiaBal = [
    contract.functions.bals(i).call()
    for i in range(7)
]
pprint(asiaBal)

# transact
hash1 = contract.functions.give('', charity, 0, 0, '', '').transact()
pprint(hash1)

# deploy
with open('contract/bytecode.json') as f:
    bytecode = json.load(f)['object']

# https://web3py.readthedocs.io/en/stable/contracts.html#contract-deployment-example
Greeter = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Greeter.constructor().transact()
tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
address = tx_receipt.contractAddress
greeter = web3.eth.contract(abi=abi, address=address)
pprint(address)

asiaBal = [
    greeter.functions.bals(i).call()
    for i in range(7)
]
pprint(asiaBal)
