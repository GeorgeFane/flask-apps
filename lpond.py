from flask import Flask, render_template, request, Blueprint
from ming import convert

lpond = Blueprint('lpond', __name__)

@lpond.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@lpond.route('/', methods=['GET', 'POST'])
def index():
    post = request.method == 'POST'
    if post:
        convert(request.form)
    return render_template("lpond.html", post=post)
