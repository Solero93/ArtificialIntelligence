"""Build a sentiment analysis / polarity model

Sentiment analysis can be casted as a binary text classification problem,
that is fitting a linear classifier on features extracted from the text
of the user messages so as to guess wether the opinion of the author is
positive or negative.

In this examples we will use a movie review dataset.

"""
# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: Simplified BSD

import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import os

if __name__ == "__main__":
    # NOTE: we put the following in a 'if __name__ == "__main__"' protected
    # block to be able to use a multi-core grid search that also works under
    # Windows, see: http://docs.python.org/library/multiprocessing.html#windows
    # The multiprocessing module is used as the backend of joblib.Parallel
    # that is used when n_jobs != 1 in GridSearchCV

    # the training data folder must be passed as first argument
    movie_reviews_data_folder = os.path.dirname(os.path.realpath(__file__))+"/data/movie_reviews/txt_sentoken/" #sys.argv[1]
    dataset = load_files(movie_reviews_data_folder, shuffle=False)
    
    print("n_samples: %d" % len(dataset.data))
    print("\n Example of one document in the training set:")
    print("\n ----------------------------------- \n")
    print(dataset.data[0]) 
    print("\n ----------------------------------- \n")
    print("Its classification: "+dataset.target_names[dataset.target[0]]) 

    # split the dataset in training and test set:
    docs_train, docs_test, target_train, target_test = train_test_split(
        dataset.data, dataset.target, test_size=0.25, random_state=None)

    predicted = []
    
    # TASK: Build a vectorizer / classifier pipeline that filters out tokens
    # that are too rare or too frequent


    # TASK: Build a grid search to find out whether unigrams or bigrams are
    # more useful.
    # Fit the pipeline on the training set using grid search for the parameters
    

    # TASK: print the cross-validated scores for the each parameters set
    # explored by the grid search
   

    # TASK: Predict the outcome on the testing set and store it in a variable
    # named predicted
    

    # Print the classification report
    #print("\n"+metrics.classification_report(target_test, predicted,target_names=dataset.target_names))

    # Print and plot the confusion matrix
    #cm = metrics.confusion_matrix(target_test, predicted)
    #print(cm)

    # import matplotlib.pyplot as plt
    # plt.matshow(cm)
    # plt.show()

    
    print("\nPrediction examples:\n")

    reviews = ["This movie is really really bad, please do not see it!", "I love this movie, great story and hilarious script"]

    
    # TASK: Predict the outcome on the reviews set and store it in a variable named predicted 
    predicted = [-1,-1]
    

    for review, category in zip(reviews, predicted):
        print('%r => %s' % (review, 'your prediction here'))
