from flask import *
import json
import pandas
import os

artist = Blueprint('artist', __name__, template_folder='templates')

script_dir = os.path.dirname(__file__)
with open(
    os.path.join(script_dir, 'data/freqs.txt')
) as f:
    freqs = json.load(f)
with open(
    os.path.join(script_dir, 'data/correct.txt')
) as f:
    correct = json.load(f)

@artist.route('/', methods=['GET', 'POST'])
def index():
    post = request.method == 'POST'
    if post:
        inp = request.form['name']
        key = inp.lower()
        if key in correct:
            return redirect(url_for('artist.result', encoded=correct[key]))
        else:
            return render_template('artist.html', post=post, inp=inp)
    else:
        return render_template('artist.html', post=post)

@artist.route('/<encoded>/')
def result(encoded):
    name = encoded.replace('%20', ' ')
    dic = freqs[name].items()
    df = pandas.DataFrame.from_dict(dic)
    df.columns = ['Lyric', 'Frequency']

    return render_template(
        'result.html',
        name=name,
        tables=[df.to_html(classes='data', header="true")]
    )