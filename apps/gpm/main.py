from flask import *
import numpy as np
from itertools import product
import pandas as pd
import json
from collections import Counter

gpm = Blueprint('gpm', __name__, template_folder='templates')

@gpm.route('/', methods=['GET', 'POST'])
def index():
    p = 2
    s = 2
    matrix = ''

    if request.method == 'POST':
        data = request.form
        p = int(data['p'])
        s = int(data['s'])
        matrix = data['matrix']

        if matrix:
            a = np.array(json.loads(matrix))
        else:
            n = p * s ** p
            row = np.arange(n)
            np.random.shuffle(row)
            
            shape = [s] * p + [p]
            a = row.reshape(shape)
            matrix = json.dumps(a.tolist())

        cords = list(product(np.arange(s), repeat=p-1)) 
        locals = []
        for i in range(p):
            b = a.swapaxes(i, p).take(i, axis=i) 

            for cord in cords:
                copy = list(cord)
                copy.insert(i, b[cord].argmax()) 
                locals.append(tuple(copy))

        freqs = Counter(locals)
        opts = [x for x, y in freqs.items() if y == p]

        df = pd.DataFrame(zip(
            opts,
            [a[opt] for opt in opts]
        ), columns=['Index', 'Payoffs'])
        
    return render_template(
        'gpm.html', 
        p=p, s=s, 
        matrix=matrix, 
        tables=[
            df.to_html(classes='data', header="true")
        ] if matrix else []
    )