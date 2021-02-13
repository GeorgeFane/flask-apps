from flask import *
import pandas as pd
from math import floor

import json
from web3 import Web3, HTTPProvider
import datetime, pytz

#sets up web3
url = 'https://sandbox.truffleteams.com/apikey'
web3 = Web3(HTTPProvider(url))

acc = web3.eth.accounts
user, charity, store = acc[:3]

headers = ['TimestampEST', 'From', 'To', 'Continent', 'Value', 'Memo', 'TxnHash']
continents = ['Asia', 'Africa', 'North America', 'South America', 'Antarctica', 'Europe', 'Australia']

with open('crypchar/contract/address.txt') as f:
    address = f.read()
with open('crypchar/contract/abi.json') as f:
    abi = json.load(f)

c = web3.eth.contract(address=address, abi=abi)
filt = c.events.trans.createFilter(fromBlock=0)

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
crypchar = Blueprint('crypchar', __name__, template_folder='templates')

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