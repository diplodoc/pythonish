from inspect import ismethod
from bs4 import BeautifulSoup
from stripogram import html2text
import json
import re
import math
import sys
import urllib2


def knn_classify(feat_vec, labl_feat_vecs, k = 5):

    def dist (a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    data = []
    for labl_feat_vec in labl_feat_vecs:
        d = dist(labl_feat_vec['data'], feat_vec)
        data.append([d, labl_feat_vec['type']])
    print data
    data.sort()
    data = data[:k]
    data = [el[1] for el in data]
    return max(set(data), key=data.count)


def create_dataset(pages):
    dataset = []
    for page in pages :
        data = form_vec(Features(), page['html'])
        dataset.append({'data': data, 'type': page['type']})
        print data
    return dataset


def form_vec(features, *args, **kwargs):
    vec = []
    for name in dir(features):
        attribute = getattr(features, name)
        if ismethod(attribute):
            vec.append(attribute(*args, **kwargs))
    return vec


def load_pages(filename):
    f = open(filename)
    return json.load(f)


class Features():

    def number_links(self, page):
        soup = BeautifulSoup(page)
        return len(soup.findAll('a'))

    def number_words(self, page):
        text = None
        try:
            text = html2text(page.encode('utf8', 'ignore'))
        except UnicodeDecodeError:
            text = html2text(page)
        return len(re.findall(r'\w+', text))


def main():
    pages = load_pages('feed-post.ls')
    #dataset = create_dataset(pages)
    url = sys.argv[1]
    html = urllib2.urlopen(url).read()
    print form_vec(Features(), html)
    #print knn_classify(form_vec(Features(), html), dataset)

main()
