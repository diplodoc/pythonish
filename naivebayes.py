"""
Implementation of the Naive Bayes algorithm
"""

import json
import math
import re

class NaiveBayes(object):
    """The NaiveBayes class implements the naive bayes algorithm"""
    def __init__(self):
        self.classes = {}
        self.vocabulary = {}
        self.priors = {}

    def train(self, classes):
        """Train the clasifier.

        The classes variable is a dictionary with the key as the class and a list
        of tokenized documents as value for every class."""
        for klass in classes:
            self.classes.setdefault(klass, {})
            self.priors.setdefault(klass, 0)
            for document in classes[klass]:
                self.priors[klass] += 1
                for item in document:
                    self.vocabulary.setdefault(item, 0)
                    self.vocabulary[item] += 1
                    self.classes[klass].setdefault(item, 0)
                    self.classes[klass][item] += 1

    def scores(self, document):
        """Returns a dictionary with the scores of the document for every class.

        The document variable must be a list with the terms of the document."""

        class_scores = {}

        vocabulary_count = len(self.vocabulary)

        for klass in self.classes:
            total_documents = float(sum(self.priors.values()))
            class_documents = float(self.priors[klass])
            score = math.log(class_documents / total_documents)

            class_word_count = float(sum(self.classes[klass].values()))

            for item in document:
                item_count = self.classes[klass].get(item, 0)
                score += math.log((item_count + 1.0) / (class_word_count + vocabulary_count))

            class_scores[klass] = score

        return class_scores

    def classify(self, document):
        """Return the class of the document.
        The document must be a list with the terms of the document."""
        scores = self.scores(document)

        predicted_class = None
        max_score = None

        for klass in scores:
            if scores[klass] > max_score:
                max_score = scores[klass]
                predicted_class = klass

        return predicted_class

    def perfomance(self, test_documents):
        """Return the accuracy of the classifier."""
        accuracy, recall, f1 = self.class_perfomance(test_documents)

        total_accuracy = sum(accuracy.values()) / float(len(accuracy))
        total_recall = sum(recall.values()) / float(len(recall))
        total_f1 = (2.0 * total_accuracy * total_recall) / (total_accuracy + total_recall)

        return total_accuracy, total_recall, total_f1

    def class_perfomance(self, test_documents):
        """Return the class accuracy of the classifier."""
        cm = {}

        for klass in test_documents:
            cm[klass] = {}
            for klass2 in test_documents:
                cm[klass][klass2] = 0

        for klass in test_documents:
            for document in test_documents[klass]:
                classification = self.classify(document)
                if classification == klass:
                    cm[klass][klass] += 1
                else:
                    cm[klass][classification] += 1

#Will be used in the future as a test
#        cm = {"a":{"a": 25, "b": 5, "c": 2},
#              "b":{"a": 3, "b": 32, "c": 4},
#              "c":{"a": 1, "b": 0, "c": 15}}

        accuracy = {}
        recall = {}
        f1 = {}

        for klass in test_documents:
            tp_fp = [cm[k][k2] 
                  for k in cm
                  for k2 in cm[k]
                  if k2 == klass]

            tp_fp = sum(tp_fp)

            accuracy[klass] = float(cm[klass][klass]) / float(tp_fp)

            tp_fn = [cm[k][k2] 
                     for k in cm
                     for k2 in cm[k]
                     if k == klass]

            tp_fn = sum(tp_fn)

            recall[klass] = float(cm[klass][klass]) / float(tp_fn)

            f1[klass] = (2.0 * accuracy[klass] * recall[klass]) / (accuracy[klass] + recall[klass])

        return accuracy, recall, f1

    def save(self, filename):
        """Save the classifier to a file."""
        classifier_data = {"classes": self.classes,
                           "vocabulary": self.vocabulary,
                           "priors": self.priors}

        with open(filename, "w") as f:
            json.dump(classifier_data, f)

    def load(self, filename):
        """Load the classifier from a file."""
        with open(filename, "r") as f:
            classifier_data = json.load(f)

        self.classes = classifier_data['classes']
        self.priors = classifier_data['priors']
        self.vocabulary = classifier_data['vocabulary']

def document_vector(document):
    terms = {}
    
    for term in document:
        terms.setdefault(term, 0)
        terms[term] += 1

    return terms

def tokenize_document(document):
    """Tokenize the contents of a document."""
    tokens = re.findall(r'\w+', document)
    
    return tokens
