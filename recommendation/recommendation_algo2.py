from __future__ import print_function

import numpy as np
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

TEST_SIZE_FRACTION = 0.5

# Load data fom files
X = np.loadtxt('digit_train_features')
y = np.loadtxt('digit_train_labels')

# Split the dataset into two equal parts
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE_FRACTION, random_state=0)

# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5, scoring='precision')
clf.fit(X_train, y_train)

print()
print("Best parameters set found on development set:")
print()
print(clf.best_estimator_)
print()
print("Grid scores on development set:")
print()
for params, mean_score, scores in clf.grid_scores_:
    print("%0.3f (+/-%0.03f) for %r"
          % (mean_score, scores.std() / 2, params))
print()

print("Detailed classification report:")
print()
y_true, y_pred = y_test, clf.predict(X_test)
print(classification_report(y_true, y_pred))

print("Predicted values:")
print()
X_eval = np.loadtxt('digit_test_features')
y_eval = clf.predict(X_eval)
print(y_eval)
