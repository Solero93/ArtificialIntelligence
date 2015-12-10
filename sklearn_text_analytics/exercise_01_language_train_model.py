"""Build a language detector model

The goal of this exercise is to train a linear classifier on text features
that represent sequences of up to 3 consecutive characters so as to be
recognize natural languages by using the frequencies of short character
sequences as 'fingerprints'.

"""
# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: Simplified BSD

import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn import metrics

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC

# The training data folder must be passed as first argument
languages_data_folder = os.path.dirname(os.path.realpath(__file__))+"/data/languages/paragraphs/" #sys.argv[1]
dataset = load_files(languages_data_folder)

print("n_samples: %d" % len(dataset.data))
print("\n Example of one document in the training set:")
print("\n ----------------------------------- \n")
print(dataset.data[0]) 
print("\n ----------------------------------- \n")
print("Its classification: "+dataset.target_names[dataset.target[0]]) 
    
# Split the dataset in training and test set:
docs_train, docs_test, target_train, target_test = train_test_split(
    dataset.data, dataset.target, test_size=0.5)



# TASK: Build a an vectorizer that splits strings into sequence of 1 to 3
# characters instead of word tokens

 

# TASK: Build a vectorizer / classifier pipeline using the previous analyzer
# the pipeline instance should stored in a variable named clf


# TASK: Fit the pipeline on the training set


# TASK: Predict the outcome on the testing set in a variable named predicted


# Print the classification report
#print(metrics.classification_report(target_test, predicted, target_names=dataset.target_names))


# Plot the confusion matrix
#cm = metrics.confusion_matrix(target_test, predicted)
#print(cm)

#import pylab as pl
#pl.matshow(cm, cmap=pl.cm.jet)
#pl.show()

# Predict the result on some short new sentences:
print("\nPrediction examples:\n")
sentences = [
    u'This is a language detection test.',
    u'Ceci est un test de d\xe9tection de la langue.',
    u'Dies ist ein Test, um die Sprache zu erkennen.',
]


# TASK: Predict the outcome on the sentences in a variable named predicted
predicted = [-1,-1,-1]

for s, p in zip(sentences, predicted):
    print(u'The language of "%s" is "%s"' % (s, 'your prediction here'))
