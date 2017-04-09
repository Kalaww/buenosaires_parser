import collections
import nltk
import numpy
from sklearn.svm import LinearSVC, SVC, NuSVC
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.metrics.scores import precision, recall

from src.extract import Extractor

classifier_nom = None
classifier_prenom = None
classifier_condition = None


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

    def classify_prob(self, featureset):
        return self.classifier.classify_many([featureset])[0]

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

        for tag in refset.keys():
            prc = precision(refset[tag], testset[tag])
            rec = recall(refset[tag], testset[tag])
            print('{}: precision={:4.2f} recall={:4.2f}'.format(tag, prc, rec))


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

        self.train_set = setup_features(target, train_set)
        self.test_set = setup_features(target, test_set)

    def split_dataset(self):
        size_data = len(self.data)
        numpy.random.shuffle(self.data)
        nb_train = int(size_data * 0.8)
        return self.data[:nb_train], self.data[nb_train:]



def setup_features(target, set):
    features = None
    if (target == 'nom'):
        features = nom_features
    elif (target == 'prenom'):
        features = prenom_features
    elif (target == 'condition'):
        features = condition_features

    if (features is None):
        return

    return nltk.classify.apply_features(features, set)

def nom_features(word):
    return {
        'length' : len(word['word']),
        'before' : word['before'],
        'after' : word['after'],
        'n_upper' : ratio_nb_uppercase(word['word']),
        'after_tag' : word['after_tag'],
        'before_tag' : word['before_tag'],
        'word': word['word']
    }

def prenom_features(word):
    return {
        'length' : len(word['word']),
        'before' : word['before'],
        'after' : word['after'],
        'f_upper' : is_first_uppercase(word['word']),
        'after_tag' : word['after_tag'],
        'before_tag' : word['before_tag'],
        'word': word['word']
    }

def condition_features(word):
    return {
        'length': len(word['word']),
        'before' : word['before'],
        'after' : word['after'],
        'after_tag' : word['after_tag'],
        'before_tag' : word['before_tag'],
        'word': word['word']
    }

def ratio_nb_uppercase(word):
    return sum(1 for l in word if l.isupper()) / len(word)

def is_first_uppercase(word):
    return word[0].isupper()

def setup_classifier(filename, target, method, verbose=False):
    ex = Extractor(filename)
    words = ex.extract_personnes_words()

    for i, item in enumerate(words):
        if (item[1] != target):
            words[i] = (item[0], 'other')

    cl = Classifier(words)
    cl.setup(target, method)

    if verbose :
        print('Informations on \'{}\' classification'.format(target))
        cl.print_accuracy()
        cl.print_precision_recall()
        if method == 'naive_bayes' :
            cl.classifier.show_most_informative_features(5)
    return cl

def setup_classifiers(f_learning_set, method, verbose=False):
    global classifier_prenom, classifier_nom, classifier_condition
    print('setting up classifiers based on data in file {}'.format(f_learning_set))
    classifier_prenom = setup_classifier(f_learning_set, 'prenom', method, verbose)
    classifier_nom = setup_classifier(f_learning_set, 'nom', method, verbose)
    classifier_condition = setup_classifier(f_learning_set, 'condition', method, verbose)


def best_prob_classify(word):
    prob_prenom = classifier_prenom.classify_prob(prenom_features(word))
    prob_nom = classifier_nom.classify_prob(nom_features(word))
    prob_condition = classifier_condition.classify_prob(condition_features(word))

    max = 'other'
    max_prob = 0.0
    if(prob_prenom.prob('prenom') > prob_prenom.prob('other')):
        max = 'prenom'
        max_prob = prob_prenom.prob('prenom')
    else:
        max = 'other'
        max_prob = prob_prenom.prob('other')

    if(prob_nom.prob('nom') > prob_nom.prob('other')):
        if(prob_nom.prob('nom') > max_prob):
            max = 'nom'
            max_prob = prob_nom.prob('nom')
    else:
        if(prob_nom.prob('other') > max_prob):
            max = 'other'
            max_prob = prob_nom.prob('other')

    if(prob_condition.prob('condition') > prob_condition.prob('other')):
        if(prob_condition.prob('condition') > max_prob):
            max = 'condition'
            max_prob = prob_condition.prob('condition')
    else:
        if(prob_condition.prob('other') > max_prob):
            max = 'other'
            max_prob = prob_condition.prob('other')

    return max, max_prob


def best_classify(word):
    is_prenom = 1 if classifier_prenom.classify_prob(prenom_features(word)) == 'prenom' else 0
    is_nom = 1 if classifier_nom.classify_prob(nom_features(word)) == 'nom' else 0
    is_condition = 1 if classifier_condition.classify_prob(condition_features(word)) == 'condition' else 0

    total = is_prenom + is_nom + is_condition
    if total != 1 :
        return 'other'
    if is_prenom == 1 :
        return 'prenom'
    if is_nom == 1 :
        return 'nom'
    return 'condition'