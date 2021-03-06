import json
import requests
from web3 import Web3, HTTPProvider
from flask import *
import os

chant = Blueprint('chant', __name__, template_folder='templates')

TRUFFLE = os.getenv('TRUFFLE')
url= 'https://sandbox.truffleteams.com/' + TRUFFLE
w3 = Web3(HTTPProvider(url))
w3.eth.default_account = w3.eth.accounts[0]

script_dir = os.path.dirname(__file__)
with open(
    os.path.join(script_dir, 'contract/address.txt')
) as f:
    address = f.read()
with open(
    os.path.join(script_dir, 'contract/abi.json')
) as f:
    abi = json.load(f)
c = w3.eth.contract(abi=abi, address=address)

@chant.route('/')
def hello():
    return redirect(url_for('chant.index', parent=0))

@chant.route('/<parent>', methods=['POST', 'GET'])
def index(parent):
    if request.method == 'POST':
        data = request.form
        c.functions.store(
            data['message'], 
            parent
        ).transact()

    away = not parent == '0'
    if away:
        receipt = w3.eth.getTransactionReceipt(parent)
        processed = c.events.post().processReceipt(receipt)
    op = processed[0] if away else False

    event_filter = c.events.post.createFilter(
        fromBlock=0, 
        argument_filters=dict(
            parent=parent if parent else '0'
        )
    )
    entries = event_filter.get_all_entries()

    return render_template(
        'chant.html',
        entries=entries,
        op=op
    )

#chant.run(port=8080, debug=True)