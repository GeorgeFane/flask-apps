import requests
from flask import *
import concurrent.futures
import numpy as np
import pandas as pd
from secrets import *

url = 'http://www.omdbapi.com'
apikey = access('omdb')

watchlist = Blueprint('watchlist', __name__, template_folder='templates')

@watchlist.route('/', methods=['GET', 'POST'])
def index():
    return render_template(
        'watchlist.html',
        favs={}
    )