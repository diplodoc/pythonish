from stripogram import html2text
import sys
import httplib2


if __name__ == '__main__':
    http = httplib2.Http()
    headers, body = http.request(sys.argv[1])
    ctype = headers['content-type']
    charset = ctype[ctype.index('charset=')+8:]
    body = body.decode('UTF-8')
    try:
        text = html2text(body.encode('utf8', 'ignore'))
    except UnicodeDecodeError:
        text = html2text(body)
    print text