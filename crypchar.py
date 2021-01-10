from flask import *
import pandas as pd
from math import floor

import json
from web3 import Web3, HTTPProvider
import datetime, pytz

#sets up web3
url = 'https://sandbox.truffleteams.com/8f7572d1-e253-420a-93bc-2ed8a6f051e6'
web3 = Web3(HTTPProvider(url))

acc = web3.eth.accounts
user, charity, store = acc[:3]

headers = ['TimestampEST', 'From', 'To', 'Continent', 'Value', 'Memo', 'TxnHash']
continents = ['Asia', 'Africa', 'North America', 'South America', 'Antarctica', 'Europe', 'Australia']

address, abi = '0x34b41A8f1b89e94F9E50283DD9F3a296C620E2fA', '[ { "anonymous": false, "inputs": [ { "indexed": false, "internalType": "bytes", "name": "TimestampEST", "type": "bytes" }, { "indexed": false, "internalType": "address", "name": "From", "type": "address" }, { "indexed": false, "internalType": "address", "name": "To", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "Continent", "type": "uint256" }, { "indexed": false, "internalType": "uint256", "name": "Value", "type": "uint256" }, { "indexed": false, "internalType": "bytes", "name": "Memo", "type": "bytes" }, { "indexed": false, "internalType": "bytes", "name": "TxnHash", "type": "bytes" } ], "name": "trans", "type": "event" }, { "stateMutability": "payable", "type": "fallback" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "bals", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "time", "type": "string" }, { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "cont", "type": "uint256" }, { "internalType": "uint256", "name": "value", "type": "uint256" }, { "internalType": "string", "name": "memo", "type": "string" }, { "internalType": "string", "name": "hash", "type": "string" } ], "name": "give", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "string", "name": "time", "type": "string" }, { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "cont", "type": "uint256" }, { "internalType": "uint256", "name": "value", "type": "uint256" }, { "internalType": "string", "name": "memo", "type": "string" }, { "internalType": "string", "name": "hash", "type": "string" } ], "name": "take", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" } ]'

c = web3.eth.contract(abi=abi, address=address)
filt = c.eventFilter('trans', {'fromBlock': 0,'toBlock': 'latest'})

#FUNCTIONS FOR FRONTEND
tz = pytz.timezone('America/Detroit')
now = lambda: datetime.datetime.now(tz).strftime("%m/%d/%Y, %H:%M:%S")

#transfers ether from user to charity and records it
def donate(continent, value): #value in wei
    web3.eth.defaultAccount = user
  
    hash = web3.eth.sendTransaction(
        {
            'to': charity,
            'value': value,
        }
    )
    
    c.functions.give(now(), charity, continent, value, '', hash.hex()).transact()

#transfers ether from charity to store and records it
def spend(continent, value, memo): #value in wei
    web3.eth.defaultAccount = charity
  
    hash=web3.eth.sendTransaction(
        {
            'to': store,
            'value': value,
        }
    )

    c.functions.take(now(), store, continent, value, memo, hash.hex()).transact()

first = True
crypchar = Blueprint('crypchar', __name__)

def getBals() -> list:
    return [
        dict(Continent=cont, Balance=c.functions.bals(i).call())
        for i, cont in enumerate(continents)
    ]

def getTxns() -> list:
    return [
        dict(tran['args']) 
        for tran in filt.get_all_entries()
    ]

@crypchar.route('/', methods=['GET', 'POST'])
def index():
    post = request.method == 'POST'
    global df, df1
    if post:
        data = request.form
        
        if data.get('form') == 'refresh':
            df = pd.DataFrame(getBals())
            df1 = pd.DataFrame(getTxns())

        else:
            cont = continents.index(data.get('continent'))
            value = floor(int(data.get('value')))
            
            if value < 1:
                print('error')
            else:
                if data.get('agent') == 'User':
                    donate(cont, value)
                else:
                    memo = data.get('memo')
                    spend(cont, value, memo)
                    
    if first:
        df = pd.DataFrame(getBals())
        df1 = pd.DataFrame(getTxns())

    return render_template(
        "crypchar.html",
        bals=[df.to_html(classes='data', header="true")],
        txns=[df1.to_html(classes='data', header="true")],
    )