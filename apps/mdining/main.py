from flask import *
import pandas as pd
from datetime import datetime as dt
from pytz import timezone
import requests

mdining = Blueprint(
    'mdining', __name__, 
    template_folder='templates',
    static_folder='static'
)

tz = timezone("America/Detroit")
ptime = lambda string, form: dt.strptime(string, form).time()
now = lambda: dt.now(tz).strftime('%-d %b %Y %-I:%M %p')
 
def isOpen(time):
    start, end = time.split(' ‑ ')
    return ptime(start, '%I:%M %p') < dt.now(tz).time() < ptime(end, '%I:%M %p')

@mdining.route('/')
def result():
    url = 'https://raw.githubusercontent.com/GeorgeFane/MDining-Scraper/master/scraped.txt'
    df = pd.read_csv(url, index_col=0)

    bools = [isOpen(time) for time in df['Time']]
    df.insert(0, 'isOpen', bools)

    return render_template(
        'test.html',
        table=df.to_html()
    )
