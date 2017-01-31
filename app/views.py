from flask import render_template
from flask_wtf import FlaskForm, Form
from wtforms import fields
from wtforms.validators import Required
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests 
import flask
import numpy as np
import pickle
from bs4 import BeautifulSoup

from . import app, cv, answers, answers_vecs


with open('models/input.pkl', 'rb') as picklefile:
    cv = pickle.load(picklefile)

with open('models/answers.pkl', 'rb') as picklefile:
    answers = pickle.load(picklefile)
    
with open('models/answers_vecs.pkl', 'rb') as picklefile:
    answers_vecs = pickle.load(picklefile)

class PredictForm(Form):
    """Fields for Predict"""
    myChoices = ["one", "two", "three"]
    keywords = fields.StringField('Keywords:', validators=[Required()])

    submit = fields.SubmitField('Submit')


@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    form = PredictForm()
    answer = [0,0,0,0,0]
    url = []
    username = []
    user_string = ''
    user = []
    answer_link = ''

    if form.validate_on_submit():
        # store the submitted values
        submitted_data = form.data
        print(submitted_data)

        # Retrieve values from form
        keywords = submitted_data['keywords']
        keywords_vec = cv.transform([keywords])
        indices = answers.iloc[cosine_similarity(keywords_vec, answers_vecs).argsort()[0][:-100:-1]]
        answer_id = answers.iloc[cosine_similarity(keywords_vec, answers_vecs).argsort()[0][:-5:-1]].Id.values.astype(int)[0]
        answer_link = "http://stackoverflow.com/questions/{}".format(answer_id)

        for i in range(5):
            answer[i] = indices.Body.values[i]
            current_user = indices.OwnerUserId.values.astype(int)[i]
            
            if current_user not in user:
                user.append(current_user)
            else:
                j = i + 1
                while current_user in user:
                    current_user = indices.OwnerUserId.values.astype(int)[j]    
                    j += 1
                user.append(current_user)

            url.append('http://stackoverflow.com/users/' + str(user[i]))
            response = requests.get(url[i])
            page = response.text
            soup = BeautifulSoup(page, 'lxml')
            username.append(str(soup.find('title')).split('-')[0].strip()[12:])
            
        user_string = "Users <a href={}>{}</a>, <a href={}>{}</a>, <a href={}>{}</a>, <a href={}>{}</a>, \
        and <a href={}>{}</a> can help you with your question.".format(*sum([[x,y] for x,y in zip(url, username)],[])) 

    return render_template('index.html',
        form=form,
        prediction=answer[0],
        answer_link=answer_link,
        user_string=user_string)

