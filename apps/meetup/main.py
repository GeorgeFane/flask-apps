from flask import *
import pandas as pd
from geocoder import mapquest
import os

import plotly.express as px
import plotly
import json

meetup = Blueprint('meetup', __name__, template_folder='templates')
key = os.getenv('MAPQUEST')

@meetup.route('/', methods=['GET', 'POST'])
def index():
    count = 5
    graphjson = {}

    if request.method == 'POST':
        data = request.form
        count = int(data['count'])
        address = data['address']

        addresses = data.getlist('addresses')
        addresses.append(address)
        results = [
            mapquest(x, key=key).json
            for x in addresses
            if x
        ]
        if results:
            df = pd.DataFrame(results)

            x = df.lat.mean()
            y = df.lng.mean()
            mid = mapquest((x, y), method='reverse', key=key).json
            df = df.append(mid, ignore_index=True)

            df['color'] = "Friends' Addresses"
            df.color.values[-2] = 'Your Address'
            df.color.values[-1] = 'Midpoint'

            df['size'] = 1

            fig = px.scatter_mapbox(
                df, lat="lat", lon="lng", color="color", #size='size', 
                mapbox_style="open-street-map",
                hover_data='address city'.split()
            )
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})            
            graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
    return render_template(
        'meetup.html',
        count=count,
        plot=graphjson,
    )