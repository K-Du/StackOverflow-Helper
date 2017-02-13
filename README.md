# StackOverflow-Helper

Metis Project #4 - Natural Language Processing

![webapp](webapp.png)

A Flask web app that allows one to search the most relevant Python StackOverflow answers based on keywords. This works offline but only has answers up to October 19, 2016. Uses cosine similarity to score keyword matching. Produces the top matched search result (akin to Google's I'm Feeling Lucky). The main portion of the code is in the [views.py](app/views.py) file.

To use:  

Check the dependencies and install any missing modules.   
Download the answers.csv dataset from [here.](https://www.kaggle.com/stackoverflow/pythonquestions)
Download and run the [pickler_file.py]() in the same folder where the answers.csv file is. 
This creates three pickle objects called 
Put these in a folder called 
Download the python files.




