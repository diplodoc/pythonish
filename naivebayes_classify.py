import sys
from bs4 import BeautifulSoup
from urllib2 import urlopen

from naivebayes import NaiveBayes

# example of usage: python naivebayes_classify.py http://habrahabr.ru feed-post-model.ls
# http://habrahabr.ru - page, which you wanna classify
# feed-post-model.ls - name of file with data model, built by naivebayes_train.py script

def main():
    url, model = sys.argv[1], sys.argv[2]
 
    classifier = NaiveBayes()
    classifier.load(model)

    page = urlopen(url).read()

    soup = BeautifulSoup(page)
    tags = [tag.name for tag in soup.findAll(True)]
    classification = classifier.classify(tags)

    print("Classified as: %s" % classification)

if __name__ == "__main__":
    main()