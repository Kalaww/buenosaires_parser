import collections
import nltk
import numpy
from sklearn.svm import LinearSVC, SVC, NuSVC
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.metrics.scores import precision, recall

class Classifier:

    def __init__(self, data=[]):
        self.data = data
        self.train_set = None
        self.test_set = None
        self.method = None
        self.classifier = None
        self.target = None

    def setup(self, target, method='naive_bayes', verbose=False):
        self.setup_sets(target)
        self.method = method
        self.target = target

        if(method == 'linearSVC'):
            self.classifier = SklearnClassifier(LinearSVC())
            self.classifier.train(self.train_set)
        elif(method == 'SVC'):
            self.classifier = SklearnClassifier(SVC())
            self.classifier.train(self.train_set)
        elif(method == 'nuSVC'):
            self.classifier = SklearnClassifier(NuSVC())
            self.classifier.train(self.train_set)
        else:
            self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)

        if(verbose):
            if(method == 'naive_bayes'):
                self.classifier.show_most_informative_features(5)

    def accuracy(self):
        return nltk.classify.accuracy(self.classifier, self.test_set)

    def print_accuracy(self):
        print('Accuracy: {:4.2f}'.format(self.accuracy()))

    def print_precision_recall(self):
        refset = collections.defaultdict(set)
        testset = collections.defaultdict(set)

        for i, (ft, label) in enumerate(self.test_set):
            refset[label].add(i)
            predicted = self.classifier.classify(ft)
            testset[predicted].add(i)

        target_precision = precision(refset[self.target], testset[self.target])
        target_recall = recall(refset[self.target], testset[self.target])

        print('{} precision: {:4.2f}'.format(self.target, target_precision))
        print('{} recall: {:4.2f}'.format(self.target, target_recall))

    def show_errors(self):
        errors = []
        for(ft, tag) in self.test_set:
            predicted = self.classifier.classify(ft)
            if(predicted != tag):
                errors.append((tag, predicted, ft))

        for (tag, predicted, ft) in errors:
            print('correct={}\tpredict={}\t ft={}'.format(tag, predicted, ft))


    def setup_sets(self, target):
        train_set, test_set = self.split_dataset()

        features = None
        if(target == 'nom'):
            features = nom_features
        elif(target == 'prenom'):
            features = prenom_features

        if(features is None):
            return

        self.train_set = nltk.classify.apply_features(features, train_set)
        self.test_set = nltk.classify.apply_features(features, test_set)

    def split_dataset(self):
        size_data = len(self.data)
        numpy.random.shuffle(self.data)
        nb_train = int(size_data * 0.8)
        return self.data[:nb_train], self.data[nb_train:]


def nom_features(word):
    return {
        'before' : word[1],
        'after' : word[2]
    }

def prenom_features(word):
    return {
        'before' : word[1],
        'after' : word[2]
    }

def ratio_nb_uppercase(word):
    return sum(1 for l in word if l.isupper()) / len(word)
