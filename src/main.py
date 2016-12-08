# -*- coding: utf-8 -*-

import re
from magic import Magic
import logging
import cst

def actes_from_file(filename):
    actes = []
    with open(filename, 'r') as fd:
        for line in fd.readlines():
            line = re.sub('\s\s+', ' ', line)
            m = re.search('(\<ACTE.+/ACTE\>)', line)
            if (m is not None):
                actes.append(m.string[m.start(1):m.end(1)])
    return actes


def extract_train_acte(filename_in, filename_out):
    with open(filename_in, 'r') as fd_in, open(filename_out, 'w+') as fd_out:
        for line in fd_in.readlines():
            if '<nom>' in line:
                line = re.sub('\s\s+', ' ', line)
                fd_out.write(line)


def tag_multiple_actes(filename_in, filename_out):
    with open(filename_in, 'r') as fd_in, open(filename_out, 'w+') as fd_out:
        for line in fd_in.readlines():
            line = re.sub('\s\s+', ' ', line)
            m = re.search('(\<ACTE.+/ACTE\>)', line)
            if m is not None:
                magic = Magic(m.string[m.start(1):m.end(1)], method='text')
                magic.run()
                fd_out.write(magic.tostring())
            else:
                fd_out.write(line)
            fd_out.write("\n")

logging.basicConfig(filename=cst._LOG_FILE, level=logging.INFO, filemode='w')

# extract_train_acte(cst._BUENOS_AIRES, cst._BUENOS_AIRES_TRAIN)


tag_multiple_actes('../test/one_acte.xml', cst._MATRIMONIOS_TAGGED)