from stripogram import html2text
from collections import defaultdict
import re
import sys
import json

def get_words(text):
    return re.compile('\w+').findall(text)

if __name__ == "__main__":

    f_in = open(sys.argv[1])
    f_out = open(sys.argv[2], 'w')
    pages = json.load(f_in)
    json_doc = []
    df = defaultdict(int)
    for page in pages:
        try:
            text = html2text(page['html'].encode('utf8', 'ignore'))
        except UnicodeDecodeError:
            text = html2text(page['html'])
        words = get_words(text)
        n = len(words)
        tf = defaultdict(int)
        for word in words: tf[word] +=1
        for word in tf: tf[word] /= float(n)
        json_doc.append({'url': page['url'], 'features': tf})
        words_set = set(words)
        for word in words_set: df[word] +=1
    n = len(pages)
    for word in df: df[word] /= float(n)
    for row in json_doc:
        features = row['features']
        for word in features:
            if word in df:
                features[word] /= float(df[word])
            else :
                del features[word]
        row['features'] = features
    json_doc.append(df)
    f_out.write(json.dumps(json_doc))
    f_in.close()
    f_out.close()