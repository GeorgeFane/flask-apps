from flask import *
app = Flask(__name__)

names = [
    'Lyric Frequency',
    'Datastore Interface',
    'CryptoCharity',
    'Payoff Matrix Solver',
    'RatingsMap',
]

routes = [
    'artist',
    'dstore',
    'crypchar',
    'gpm',
    'heatmap'
]

from artist import artist
app.register_blueprint(artist, url_prefix='/artist')

from dstore import dstore
app.register_blueprint(dstore, url_prefix='/dstore')

from crypchar import crypchar
app.register_blueprint(crypchar, url_prefix='/crypchar')

from gpm import gpm
app.register_blueprint(gpm, url_prefix='/gpm')

from heatmap import heatmap
app.register_blueprint(heatmap, url_prefix='/heatmap')

@app.route('/')
def hello_world():
    return render_template(
        'main.html',
        apps=list(zip(names, routes))
    )

if __name__ == '__main__':
    app.run(port=8080, debug=True)