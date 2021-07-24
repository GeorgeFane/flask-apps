from flask import Flask, render_template

from apps.artist.main import artist
from apps.dstore.main import dstore
from apps.crypchar.main import crypchar
from apps.gpm.main import gpm
from apps.ratingsmap.main import ratingsmap
from apps.chant.main import chant
from apps.mdining.main import mdining
from apps.meetup.main import meetup

app = Flask(__name__)
app.register_blueprint(artist, url_prefix='/artist')
app.register_blueprint(dstore, url_prefix='/dstore')
app.register_blueprint(crypchar, url_prefix='/crypchar')
app.register_blueprint(gpm, url_prefix='/gpm')
app.register_blueprint(ratingsmap, url_prefix='/ratingsmap')
app.register_blueprint(chant, url_prefix='/chant')
app.register_blueprint(mdining, url_prefix='/mdining')
app.register_blueprint(meetup, url_prefix='/meetup')

apps = {
    'Lyric Frequency': 'artist',
    'Datastore Query Interface': 'dstore',
    'CryptoCharity': 'crypchar',
    'Payoff Matrix Solver': 'gpm',
    'RatingsMap': 'ratingsmap',
    'Chant Platform': 'chant',
    'M|Dining Scraper': 'mdining',
    'MeetUp': 'meetup'
}


@app.route('/')
def index():
    return render_template(
        'main.html',
        apps=apps.items()
    )


if __name__ == '__main__':
    app.run(port=8080, debug=True)
