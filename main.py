from flask import *
from artist import artist
from dstore import dstore
from lpond import lpond
from crypchar import crypchar

app = Flask(__name__)
app.register_blueprint(artist, url_prefix='/artist')
app.register_blueprint(dstore, url_prefix='/dstore')
app.register_blueprint(lpond, url_prefix='/lpond')
app.register_blueprint(crypchar, url_prefix='/crypchar')

@app.route('/')
def hello_world():
    return render_template(
        'index.html',
        apps={
            'Lyric Frequency': 'artist',
            'Datastore Query Interface': 'dstore',
            #'Counterpoint Checker': 'lpond',
            'CryptoCharity': 'crypchar',
        }
    )

if __name__ == '__main__':
    app.run(port=8080, debug=True)