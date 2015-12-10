from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn import metrics
from sklearn.grid_search import GridSearchCV
import os


#We will work with 4 categories
categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']


##############################   Loading data    ##############################

print("\n ---- Loading 20 newsgroups dataset filtering categories: %r" % categories)

data_train = fetch_20newsgroups(data_home=os.path.dirname(os.path.realpath(__file__))+'/data/twenty_newsgroups/', subset='train', categories=categories, shuffle=True, random_state=42)
data_test = fetch_20newsgroups(data_home=os.path.dirname(os.path.realpath(__file__))+'/data/twenty_newsgroups/', subset='test', categories=categories,shuffle=True, random_state=42)


print('data loaded, %d documents for training' % len(data_train.data))

print("\n Example of one document in the training set:")
print("\n ----------------------------------- \n")
print(data_train.data[0])
print("\n ----------------------------------- \n")
print("Its classification: "+data_train.target_names[data_train.target[0]]) 


#################################   Extracting Features    ############################

#Bag of words: assign a number to each word in the corpus and store in x[i,j] the ocurrences of word j in document i

print("\n ---- Extracting features from the training data")

#YOUR CODE HERE
count_vect = CountVectorizer()
x_train_count = count_vect.fit_transform(data_train.data)

#################################   From occurrences to frequencies   ############################

# longer documents will have higher count values
# so lets  divide the number of occurrences of each word in a document by the total number of words in the document
# also, lets downscale weights for words that occur in many documents and are therefore less informative 
# tf= term frequency, and tf-idf = term frecuency times inverse document frequency

print("\n---- Normalizing features to a tf-idf representation")

#YOUR CODE HERE
tfidf_transformer = TfidfTransformer()
x_train_tfidf = tfidf_transformer.fit_transform(x_train_count)

print("n_samples: %d, n_features: %d" % x_train_tfidf.shape)

#################################   Training   ############################

# we fit the classifier with the frequencies of each word in a document and the classification of the document

print("\n---- Training classifier")

#YOUR CODE HERE

# print ("target1: ", data_train.target_names[data_train.target[0]])
learner_mnNB = MultinomialNB()
clf = learner_mnNB.fit(x_train_tfidf, data_train.target)

#################################   Predict   ############################

#To predict, we extract the same features from the test documents
#Or, we use a pipeline with the original documents


print("\n---- Predicting 2 new documents")

new_docs = ['God is love', 'OpenGL on the GPU is fast']
x_new_count = count_vect.transform(new_docs)
x_new_tfidf = tfidf_transformer.transform(x_new_count)
predicted = clf.predict(x_new_tfidf)

#YOUR CODE HERE

for doc, category in zip(new_docs, predicted):
    print('%r => %s' % (doc, data_train.target_names[category]))


#or directly use the pipeline with the original test documents
print("\n---- Predicting with the test dataset")
docs_test = data_test.data
predicted = []

#YOUR CODE HERE

"""
Debería hacer algo aquí con lo que se aprendió, pero no hay tiempo, ni ganas
"""

#################################   Statistics   ############################

#Calculating the precision
print("\n Precision Naive Bayes classifier:" )  
#YOUR CODE HERE
print("\n Classification Report")
#YOUR CODE HERE
print("\n Confusion matrix")
#YOUR CODE HERE


#################################   Parameter tunning   ############################

#we run an exhaustive search of the best parameters on a grid of possible values

#YOUR CODE HERE
