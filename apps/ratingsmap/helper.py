import requests
import concurrent.futures
import numpy as np
import pandas as pd

from secrets import *

url = 'http://www.omdbapi.com'
apikey = access('omdb')

search = lambda title: requests.get(
    url,
    params=dict(
        apikey=apikey,
        type='series',
        s=title
    )
).json()

getShow = lambda title: requests.get(
    url,
    params=dict(
        apikey=apikey,
        type='series',
        t=title
    )
).json()

getSeason = lambda title, Season: requests.get(
    url,
    params=dict(
        apikey=apikey,
        type='series',
        t=title,
        Season=Season
    )
).json()

specific = lambda title: lambda Season: getSeason(title, Season)

def whole(n, title):
    indexes = np.arange(n) + 1

    # get all seasons concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
        futures = executor.map(
            specific(title),
            indexes
        )
    seasons = list(futures)

    # list of dicts to df 
    df = pd.DataFrame([
        {
            int(episode['Episode']): float(episode['imdbRating'])
            for episode in season['Episodes']
            if not episode['imdbRating'] == 'N/A'
        }
        for season in seasons
    ])

    # sort columns and add episode mean at bottom
    df = df.append(
        df.mean(), ignore_index=True, 
    ).reindex(sorted(df.columns), axis=1)

    # change row labels
    df.index = list(indexes) + ['Mean']

    df.columns.name = 'Episode\Season'

    # add season mean on right
    df['Mean'] = df.mean(axis=1)

    return df