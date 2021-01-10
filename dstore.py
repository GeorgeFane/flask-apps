from flask import *
import os
import pandas as pd
from google.cloud import datastore

dstore = Blueprint('dstore', __name__)

path = 'data/datastore-creds.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
client = datastore.Client()

@dstore.route('/', methods=['POST'])
def indexpost():
    query = client.query(kind=request.form['kind']) 

    prop = request.form['property']
    op = request.form['operator']
    value = request.form['value']

    if prop and op and value:   
        if request.form.get('int'):
            value = int(value)
        query.add_filter(prop, op, value)

    fetched = list(query.fetch())
    df = pd.DataFrame(fetched)

    return render_template(
        'dstore.html', 
        tables=[df.to_html(classes='data', header="true")]
    )

@dstore.route('/')
def index():
    return render_template('dstore.html', tables=None)