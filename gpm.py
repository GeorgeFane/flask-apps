from flask import *
import numpy as np
from itertools import product
import pandas as pd
from datetime import datetime as dt
import json
from collections import Counter

gpm = Blueprint('gpm', __name__)

@gpm.route('/', methods=['GET', 'POST'])
def index():
    p = 2
    s = 2
    matrix = ''
    table = [['None', 'None']]

    if request.method == 'POST':
        data = request.form
        p = int(data['p'])
        s = int(data['s'])
        matrix = data['matrix']
        
        start = dt.now()

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

        if opts:
            table = list(zip(
                opts,
                [a[opt] for opt in opts]
            ))
        
    return render_template('gpm.html', p=p, s=s, matrix=matrix, table=table)