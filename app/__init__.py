from flask import Flask
import pickle

with open('models/input.pkl', 'rb') as picklefile:
    cv = pickle.load(picklefile)

with open('models/answers.pkl', 'rb') as picklefile:
    answers = pickle.load(picklefile)
    
with open('models/answers_vecs.pkl', 'rb') as picklefile:
    answers_vecs = pickle.load(picklefile)

app = Flask(__name__)
# app.config.from_object("app.config")
app.config.update(dict(
	SECRET_KEY="testing"
))

from .views import *

# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    """Page Not Found"""
    return render_template('404.html'), 404
