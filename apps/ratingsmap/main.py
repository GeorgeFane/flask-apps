from flask import *
from apps.ratingsmap.helper import *

ratingsmap = Blueprint('ratingsmap', __name__, template_folder='templates')
admin = False

@ratingsmap.route('/', methods=['GET', 'POST'])
def index():
    print('admin', admin)
    if request.method == 'POST':
        data = request.form
        return redirect(
            url_for(
                'ratingsmap.results', query=data['search']
            )
        )
    else:
        return render_template(
            'index.html',
        )

@ratingsmap.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form

        global admin
        admin = data['user'] == 'george'
        print(admin)

        return redirect(
            url_for('ratingsmap.index')
        )
    else:
        return render_template(
            'login.html',
        )

@ratingsmap.route('/<query>/')
def results(query):
    resp = search(query)
    error = resp.get('Error', '')
    results = resp.get('Search', [])

    return render_template(
        'results.html', 
        error=error,
        results=results,
    )

@ratingsmap.route('/show/<title>/')
def show(title):
    error = ''

    show = getShow(title)
    poster = show['Poster']

    try:
        n = int(show['totalSeasons'])
        df = whole(n, title)
        styled = (
            df.T
        ).style.background_gradient(axis=None)

    except:
        error = 'No Seasons'

    return render_template(
        'show.html', 
        tables=[styled.render()] if styled else [],
        error=error,
        poster=poster,
    )