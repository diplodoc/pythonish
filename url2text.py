from stripogram import html2text
from urllib2 import urlopen
import sys

if __name__ == '__main__':
    print html2text(urlopen(sys.argv[1]).read())
