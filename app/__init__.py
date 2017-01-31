from flask import Flask
from sklearn.externals import joblib
import pickle

app = Flask(__name__)
app.config.from_object("app.config")


with open(u'models/input.pkl', 'rb') as picklefile:
    cv = pickle.load(picklefile)

with open(u'models/answers.pkl', 'rb') as picklefile:
    answers = pickle.load(picklefile)
    
with open(u'models/answers_vecs.pkl', 'rb') as picklefile:
    answers_vecs = pickle.load(picklefile)


from .views import *


# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    """Page Not Found"""
    return render_template('404.html'), 404
