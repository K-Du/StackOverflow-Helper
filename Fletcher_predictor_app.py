import flask
#from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



# Train a model at the beginning; this guy will stay in memory the whole
# time our server is up!

# The example training data has a single feature and for all training X
# values from 1 to 500 the true response is 0; for all X values from 500
# to 1000 the true response is 1. Pretty simple decision boundary here,
# the model is if you encounter x < 500, classify as 0, if 500 < x,
# classify as 1.

# You could also load a pickled model rather than training on server
# launch, which would be more typical.

import pickle

with open('/Users/kevin/fletcher/data/input.pkl', 'rb') as picklefile:
    cv = pickle.load(picklefile)

with open('/Users/kevin/fletcher/data/answers.pkl', 'rb') as picklefile:
    answers = pickle.load(picklefile)
    
with open('/Users/kevin/fletcher/data/answers_vecs.pkl', 'rb') as picklefile:
    answers_vecs = pickle.load(picklefile)


# Initialize the app

app = flask.Flask(__name__)


# An example of routing:
# If they go to the page "/" (this means a GET request
# to the page http://127.0.0.1:5000/), return a simple
# page that says the site is up!

@app.route("/")
def hello():
    return "It's alive!!!"


# Let's turn this into an API where you can post input data and get
# back output data after some calculations.

# If a user makes a POST request to http://127.0.0.1:5000/predict, and
# sends an X vector (to predict a class y_pred) with it as its data,
# we will use our trained LogisticRegression model to make a
# prediction and send back another JSON with the answer. You can use
# this to make interactive visualizations.

@app.route("/yo")
def hello2():
    return "?!!"


@app.route("/predict", methods=["POST"])
def predict():

    # read the data that came with the POST request as a dict
    data = flask.request.json

    # let's convert this into a numpy array so that we can
    # stick it into our model
    
    x = cv.transform(data["example"])
    sorted(cosine_similarity(x, answers_vecs)[0])[-5:]
    ANSWER = answers.iloc[cosine_similarity(x, answers_vecs).argsort()[0][:-5:-1]].Body.values[0]
    # Classify!
    
    y_pred = 0
    
    # Turn the result into a simple list so we can put it in
    # a json (json won't understand numpy arrays)

    # Put the result in a nice dict so we can send it as json
    results = {"predicted": ANSWER}
    # Return a response with a json in it
    # flask has a quick function for that that takes a dict
    return flask.jsonify(results)


# Start the server, continuously listen to requests.
# We'll have a running web app!

# For local development:
app.run(debug=True)

# For public web serving:
# app.run(host='0.0.0.0')
