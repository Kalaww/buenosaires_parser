# -*- coding: utf-8 -*-
import nltk
import database
import re
from magic import Magic

# Découper un acte avec des stopwords(',', 'Ts.:', 'y', 'y de', ':')

def distance_with_word_set(word, wordset):
    return sorted([nltk.edit_distance(word, w) for w in wordset])

def test_word(word, prenoms, noms):
    dst_prenom = distance_with_word_set(word, prenoms)
    dst_nom = distance_with_word_set(word, noms)

    print("Dst prenoms: ",dst_prenom)
    print("Dst noms: ",dst_nom)

def split_acte(acte):
    return [item.strip() for item in re.split(r'y|,|:|con|\. ', acte)]


magic = Magic('../data/acte_complete.xml', method='file')
magic.run()
