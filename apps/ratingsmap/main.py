from flask import *
from apps.ratingsmap.helper import *

ratingsmap = Blueprint('ratingsmap', __name__, template_folder='templates')
admin = False

@ratingsmap.route('/', methods=['GET', 'POST'])
def index():
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
            reviewed=list(db.collection('review').stream()),
        )

@ratingsmap.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form

        global admin
        admin = data['user'] == 'george'

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

@ratingsmap.route('/show/<title>/', methods=['GET', 'POST'])
def show(title):
    print('admin', admin)

    tables = []
    show = getShow(title)

    # check if i directly typed in name into url
    if title != show['Title']:
        return redirect(url_for(
            'ratingsmap.show', title=show['Title']
        ))        
    poster = show['Poster']

    # update review and store poster url
    if (request.method == 'POST') and admin:
        data = request.form
        db.collection('review').document(title).set({
            'review': data['review'],
            'Poster': poster
        })
    
    # get review if exists
    row = db.collection('review').document(title).get().to_dict()
    review = row['review'] if row else ''
    
    # creates heatmap if has seasons
    nstr = show.get('totalSeasons', '')
    if nstr.isdigit():
        n = int(nstr)
        df = whole(n, title)
        styled = (
            df.T
        ).style.background_gradient(
            axis=None,
        )
        tables = [styled.render()]
    
    return render_template(
        'show.html', 
        tables=tables,
        poster=poster,
        review=review
    )