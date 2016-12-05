import nltk
import numpy
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier

class Classifier:

    def __init__(self, data=[]):
        self.data = data

    def set_data(self, data):
        self.data = data

    def test(self, target, method='naive_bayes', verbose=False):
        train_set, test_set = self.get_train_and_test_set(target)

        if(method == 'svm'):
            classifier = SklearnClassifier(LinearSVC())
            classifier.train(train_set)
        else:
            classifier = nltk.NaiveBayesClassifier.train(train_set)

        accuracy = nltk.classify.accuracy(classifier, test_set)

        if(verbose):
            print('Accuracy: {:4.2f}'.format(accuracy))
            if(method == 'naive_bayes'):
                classifier.show_most_informative_features(5)

    def get_train_and_test_set(self, target):
        size_data = len(self.data)
        numpy.random.shuffle(self.data)
        nb_train = int(size_data * 0.8)

        features = None
        if(target == 'nom'):
            features = nom_features
        elif(target == 'prenom'):
            features = prenom_features

        if(features is None):
            return

        train_set = nltk.classify.apply_features(features, self.data[:nb_train])
        test_set = nltk.classify.apply_features(features, self.data[nb_train:])

        return train_set, test_set

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
