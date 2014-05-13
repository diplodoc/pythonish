from stripogram import html2text
from urllib2 import urlopen
import sys

if __name__ == '__main__':
    page = urlopen(sys.argv[1]).read()
    try:
        text = html2text(page.encode('utf8', 'ignore'))
    except UnicodeDecodeError:
        text = html2text(page)
    print text