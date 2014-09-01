from sklearn.metrics.pairwise import euclidean_distances
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

from sklearn import datasets

X = [[0, 1], [1, 1]]
y = [1, 0]
a = [[0, 0]]

scores = np.array(euclidean_distances(X, a)).transpose()
scores = list(enumerate(next(iter(scores))))
scores.sort(key=lambda x: x[1], reverse=True)

index_list = [x[0] for x in scores]
print index_list

iris = datasets.load_iris()
X = iris.data
y = iris.target

np.random.seed(0)
indices = np.random.permutation(len(X))
test_percent = 0.3
num_test = int(test_percent * len(X))

X_train = X[indices[:-num_test]]
y_train = y[indices[:-num_test]]
X_test = X[indices[-num_test:]]
y_test = y[indices[-num_test:]]

knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

print knn.predict(X_test)
print y_test