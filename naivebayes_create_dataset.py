from bs4 import BeautifulSoup
import json
import sys

#example of usage: python naivebayes_create_dataset.py feed-post.ls feed-post-tags.ls
# feed-post.ls - input filename of json with this structure:
# [{'type': 'class of the page', 'html': 'page', 'url': 'page url'}]
# feed-post-tags.ls - output filename of such json: [{'type': 'class of the page', 'tags': [list of tags on the page]}]

if __name__ == "__main__":

    f_in = open(sys.argv[1])
    f_out = open(sys.argv[2], 'w')
    pages = json.load(f_in)
    json_doc = []
    for page in pages:
        soup = BeautifulSoup(page['html'])
        tags = [tag.name for tag in soup.findAll(True)]
        json_doc.append({'type': page['type'], 'tags': tags})
    f_out.write(json.dumps(json_doc))
    f_in.close()
    f_out.close()


