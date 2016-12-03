# -*- coding: utf-8 -*-
#import nltk
#import database
import re
from magic import Magic
from extract import Extractor
import logging

def extract_train_acte(filename_in, filename_out):
    with open(filename_in, 'r') as fd_in, open(filename_out, 'w+') as fd_out:
        for line in fd_in.readlines():
            if('<nom>' in line):
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


logging.basicConfig(filename='../test/log.txt', level=logging.DEBUG, filemode='w')
# magic = Magic('../data/acte_raw.xml', method='file')
# magic.run()

# extract_train_acte('../test/buenosaires.xml', '../test/train_BA.xml')

# ex = Extractor('../test/train_BA.xml')
# train_noms = ex.get_noms()
# train_prenoms = ex.get_prenoms()
#
# print(train_prenoms)

tag_multiple_actes('../test/matrimonios.num.xml', '../test/matrimonios.date.xml')
