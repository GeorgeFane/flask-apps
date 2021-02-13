from flask import Flask, render_template
app = Flask(__name__)

names = [
    'Lyric Frequency',
    'Datastore Interface',
    'CryptoCharity',
    'Payoff Matrix Solver',
    'RatingsMap',
    'Chant Platform',
]

routes = [
    'artist',
    'dstore',
    'crypchar',
    'gpm',
    'ratingsmap',
    'chant',
]

from artist.main import artist
app.register_blueprint(artist, url_prefix='/artist')

from dstore.main import dstore
app.register_blueprint(dstore, url_prefix='/dstore')

from crypchar.main import crypchar
app.register_blueprint(crypchar, url_prefix='/crypchar')

from gpm.main import gpm
app.register_blueprint(gpm, url_prefix='/gpm')

from ratingsmap.main import ratingsmap
app.register_blueprint(ratingsmap, url_prefix='/ratingsmap')

from chant.main import chant
app.register_blueprint(chant, url_prefix='/chant')

@app.route('/')
def index():
    return render_template(
        'main.html',
        apps=list(zip(names, routes))
    )

if __name__ == '__main__':
    app.run(port=8080, debug=True)