from flask import Flask, render_template
app = Flask(__name__)

names = [
    'Lyric Frequency',
    'Datastore Query Interface',
    'CryptoCharity',
    'Payoff Matrix Solver',
    'RatingsMap',
    'Chant Platform',
    'WatchList',
]

routes = [
    'artist',
    'dstore',
    'crypchar',
    'gpm',
    'ratingsmap',
    'chant',
    'watchlist',
]

def gen():
    for route in routes:
        yield '/' + route
g = gen()

from apps.artist.main import artist
app.register_blueprint(artist, url_prefix=next(g))

from apps.dstore.main import dstore
app.register_blueprint(dstore, url_prefix=next(g))

from apps.crypchar.main import crypchar
app.register_blueprint(crypchar, url_prefix=next(g))

from apps.gpm.main import gpm
app.register_blueprint(gpm, url_prefix=next(g))

from apps.ratingsmap.main import ratingsmap
app.register_blueprint(ratingsmap, url_prefix=next(g))

from apps.chant.main import chant
app.register_blueprint(chant, url_prefix=next(g))

from apps.watchlist.main import watchlist
app.register_blueprint(watchlist, url_prefix=next(g))

@app.route('/')
def index():
    return render_template(
        'main.html',
        apps=list(zip(names, routes))
    )

if __name__ == '__main__':
    app.run(port=8080, debug=True)