from flask import *
import pandas as pd
from secrets import *

dstore = Blueprint('dstore', __name__, template_folder='templates')

@dstore.route('/', methods=['GET', 'POST'])
def indexpost():
    post = request.method == 'POST'
    if post:
        data = request.form
        table = db.collection(data['kind'])

        prop = data['property']
        op = data['operator']
        value = data['value']

        if prop and op and value:   
            if data.get('int'):
                value = int(value)
                
            table = table.where(prop, op, value)

        df = pd.DataFrame(
            [x.to_dict() for x in table.stream()]
        )

    return render_template(
        'dstore.html', 
        tables=[
            df.to_html(classes='data', header="true")
        ] if post else []
    )