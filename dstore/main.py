from flask import *
import os
import pandas as pd
from google.cloud import datastore

dstore = Blueprint('dstore', __name__, template_folder='templates')

path = 'dstore/datastore-creds.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
client = datastore.Client()

@dstore.route('/', methods=['GET', 'POST'])
def indexpost():
    post = request.method == 'POST'
    if post:
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
        tables=[
            df.to_html(classes='data', header="true")
        ] if post else []
    )