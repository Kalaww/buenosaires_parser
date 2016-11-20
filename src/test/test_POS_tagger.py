# -*- coding: utf-8 -*-
import nltk
from nltk.tag import StanfordPOSTagger
import os

os.environ["STANFORD_MODELS"] = "/home/ced/software/stanford-postagger-full-2015-12-09/models/"

sentence = u"Domingo de BELGRANO, natural de la ciudad de Oneglia, Italia, Estado de Génova, Reino de Cerdeña"

sentence = sentence.replace(",", "")
sentence = sentence.lower()

st = StanfordPOSTagger("spanish-distsim.tagger", os.environ["STANFORD_MODELS"]+"../stanford-postagger.jar")
res = st.tag(sentence.split())

for word,tag in res:
    print word+" -> "+tag
