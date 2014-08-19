from sklearn.feature_extraction.text import CountVectorizer



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


    count_vectorizer = CountVectorizer()
    count_vectorizer.fit_transform(train_set)
    print "Vocabulary:", count_vectorizer.vocabulary

    # Vocabulary: {'blue': 0, 'sun': 1, 'bright': 2, 'sky': 3}

    freq_term_matrix = count_vectorizer.transform(test_set)
    print freq_term_matrix.todense()
