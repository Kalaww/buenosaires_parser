# -*- coding: utf-8 -*-
#import nltk
#import database
import re
from magic import Magic
from extract import Extractor

# Découper un acte avec des stopwords(',', 'Ts.:', 'y', 'y de', ':')

def distance_with_word_set(word, wordset):
    return sorted([nltk.edit_distance(word, w) for w in wordset])

def test_word(word, prenoms, noms):
    dst_prenom = distance_with_word_set(word, prenoms)
    dst_nom = distance_with_word_set(word, noms)

    print("Dst prenoms: ",dst_prenom)
    print("Dst noms: ",dst_nom)

def extract_train_acte(filename_in, filename_out):
    with open(filename_in, 'r') as fd_in, open(filename_out, 'w+') as fd_out:
    	for line in fd_in.readlines():
    		if('<nom>' in line):
    			fd_out.write(line)


# magic = Magic('../data/acte_raw.xml', method='file')
# magic.run()

ex = Extractor('train_BA.xml')
ex.get_noms()
