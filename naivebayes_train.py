from random import shuffle
import sys
import json

from naivebayes import NaiveBayes

#example of usage: python naivebayes_train.py feed-post-tags.ls feed-post-model.ls
# feed-post-tags.ls - output of naivebayes_create_dataset.py script
# feed-post-model.ls - name of output file, where data model will be saved

def load_classes(dataset_file):
    classes = {}

    f = open(dataset_file)
    pages = json.load(f)

    for page in pages:
        type, tags = page['type'], page['tags']
        classes.setdefault(type, [])
        classes[type].append(tags)

    f.close()
    return classes

def split_dataset(classes, ratio):
    training_set = {}
    test_set = {}

    for type in classes:
        sep = int(len(classes[type]) * ratio)

        shuffle(classes[type])

        train, test = classes[type][:sep], classes[type][sep:]

        training_set[type] = train
        test_set[type] = test

    return training_set, test_set

def main():
    dataset_file, model = sys.argv[1], sys.argv[2]

    classes = load_classes(dataset_file)
    train, test = split_dataset(classes, 0.6)

    classifier = NaiveBayes()
    classifier.train(train)

    accuracy, recall, f1 = classifier.perfomance(test)
    print("Total perfomance")
    print("================")
    print("Accuracy: %f" % accuracy)
    print("Recall: %f" % recall)
    print("F1: %f" % f1)
    print("\n")

    class_accuracy, class_recall, class_f1 = classifier.class_perfomance(test)
    print("Class accuracy")
    print("================")
    for klass in class_accuracy:
        print("%s: %f" % (klass, class_accuracy[klass]))
    print("\n")

    print("Class recall")
    print("================")
    for klass in class_recall:
        print("%s: %f" % (klass, class_recall[klass]))
    print("\n")

    print("Class F1")
    print("================")
    for klass in class_f1:
        print("%s: %f" % (klass, class_f1[klass]))
    print("\n")

    classifier.save(model)

if __name__ == "__main__":
    main()