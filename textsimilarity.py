import sys
import json
import math
from urllib2 import urlopen
from stripogram import html2text
from textsimilarity_create_dataset import get_words
from collections import defaultdict

def cos(word_list1, word_list2):
    dot_prod, norm_a, norm_b = 0, 0, 0
    for word in word_list1:
        if word in word_list2:
            dot_prod += word_list1[word] * word_list2[word]
            norm_a += word_list1[word]**2
            norm_b += word_list2[word]**2
    norm_a = math.sqrt(norm_a)
    norm_b = math.sqrt(norm_b)
    if norm_a * norm_b < 0.000000000001 : return 0
    else: return float(dot_prod) / (norm_a * norm_b);

def get_feature_vector(words, df):
    tf = defaultdict(int)
    for word in words: tf[word] += 1
    n = len(words)
    for word in tf: tf[word] /= float(n)
    res = defaultdict(int)
    for word in tf:
        if word in df:
            res[word] = tf[word]/float(df[word])
    return res

if __name__ == '__main__':
    url, model = sys.argv[1], sys.argv[2]

    page = urlopen(url).read()
    try:
        text = html2text(page.encode('utf8', 'ignore'))
    except UnicodeDecodeError:
        text = html2text(page)

    dataset = json.load(open(model))
    texts = dataset[:-1]
    df = dataset[-1]
    vec = get_feature_vector(get_words(text), df)
    print vec
    # similarity_list = []
    # for text in texts:
    #     similarity_list.append((cos(vec, text['features']), text['url']))
    #
    # similarity_list.sort(reverse=True)
    # for entry in similarity_list