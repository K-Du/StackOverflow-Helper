
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import Required
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from . import app, cv, answers, answers_vecs

import flask
import numpy as np


class PredictForm(FlaskForm):
    """Fields for Predict"""
    myChoices = ["one", "two", "three"]
    keywords = fields.StringField('Keywords:', validators=[Required()])

    submit = fields.SubmitField('Submit')


# Initialize the app

app = flask.Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def index():

    # read the data that came with the POST request as a dict
    # data = flask.request.json
    form = PredictForm()
    answer = None
    data_point = {}

    if form.validate_on_submit():
        # store the submitted values
        submitted_data = form.data
        print(submitted_data)

        # Retrieve values from form
        keywords = submitted_data['keywords']
        x = cv.transform(keywords)
    
        answer = str(answers.iloc[cosine_similarity(x, answers_vecs).argsort()[0][:-5:-1]].Body.values[0])
        # Create array from values

    # let's convert this into a numpy array so that we can
    # stick it into our model

    # Classify!
    
    # y_pred = 0
    
    # Turn the result into a simple list so we can put it in
    # a json (json won't understand numpy arrays)

    # Put the result in a nice dict so we can send it as json
    return render_template('index.html',
        form=form,
        answer=answer)


