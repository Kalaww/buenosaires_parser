# -*- coding: utf-8 -*-
#import nltk
#import database
import re
from magic import Magic
from extract import Extractor
from classifier import Classifier
import logging

_DIR_DATA = '../test/'
_BUENOS_AIRES = _DIR_DATA + 'buenosaires.xml'
_BUENOS_AIRES_TRAIN = _DIR_DATA + 'buenosaires.train.xml'
_MATRIMONIOS_RAW = _DIR_DATA + 'matrimonios.xml'
_MATRIMONIOS_TAGGED = _DIR_DATA + 'matrimonios.tagged.xml'
_LOG_FILE = _DIR_DATA + 'log.txt'

def extract_train_acte(filename_in, filename_out):
    with open(filename_in, 'r') as fd_in, open(filename_out, 'w+') as fd_out:
        for line in fd_in.readlines():
            if('<nom>' in line):
                line = re.sub('\s\s+', ' ', line)
                fd_out.write(line)

def tag_multiple_actes(filename_in, filename_out):
    n_line = 1
    with open(filename_in, 'r') as fd_in, open(filename_out, 'w+') as fd_out:
        for line in fd_in.readlines():
            logging.debug('line %s', n_line)
            line = line.strip()
            if('</ACTE>' in line):
                magic = Magic(line, method='text')
                magic.run()
                fd_out.write(magic.tostring())
            else:
                fd_out.write(line)
            fd_out.write("\n")
            n_line += 1


logging.basicConfig(filename=_LOG_FILE, level=logging.INFO, filemode='w')

# extract_train_acte(_BUENOS_AIRES, _BUENOS_AIRES_TRAIN)

ex = Extractor(_BUENOS_AIRES_TRAIN)
noms = ex.extract_tag('nom')
prenoms = ex.extract_tag('prenom')
conditions = ex.extract_tag('condition')

total = noms + prenoms + conditions
len_noms = len(noms)
len_total = len(total)
data_noms = []
for i in range(0, len_total):
    if(i < len_noms):
        data_noms.append((total[i], 'nom'))
    else:
        data_noms.append((total[i], 'autre'))

cl = Classifier(data_noms)
cl.setup('nom', method='naive_bayes', verbose=True)
cl.print_accuracy()
cl.show_errors()
cl.print_precision_recall()

# tag_multiple_actes(_MATRIMONIOS_RAW, _MATRIMONIOS_TAGGED)
