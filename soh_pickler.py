import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer

try:
    answers = pd.read_csv(os.getcwd() + '/Answers.csv') 
except UnicodeDecodeError:
    answers = pd.read_csv(os.getcwd() + '/Answers.csv', encoding='latin-1') 

assert answers.shape == (987122, 6), 'Answers.csv file is different or improperly loaded'

answers = answers[answers.Score >= 5] # Quick way to filter dataset down to around 10% 
answers.dropna(inplace=True)

cv = CountVectorizer(stop_words='english', token_pattern="\\b[a-zA-Z][a-zA-Z]+\\b", min_df=10)
answers_vecs = cv.fit_transform(answers.Body.values)

with open(os.getcwd() + '/input.pkl', 'wb') as picklefile:
    pickle.dump(cv, picklefile)
    
with open(os.getcwd() + '/answers.pkl', 'wb') as picklefile:
    pickle.dump(answers, picklefile)
    
with open(os.getcwd() + '/answers_vecs.pkl', 'wb') as picklefile:
    pickle.dump(answers_vecs, picklefile)
