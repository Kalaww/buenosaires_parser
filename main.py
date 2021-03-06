
import sys
import getopt
import re
from src.magic import Magic
from src.classifier import setup_classifiers
import logging

import src.cst as cst

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
    n = 0
    with open(filename_in, 'r') as fd_in, open(filename_out, 'w+') as fd_out:
        for line in fd_in.readlines():
            if '<nom>' in line:
                line = re.sub('\s\s+', ' ', line)
                fd_out.write(line)
                n += 1
    print('learning set extracted with success ({} act(s))'.format(n))
    print('{} -> {}'.format(filename_in, filename_out))


def tag_multiple_actes(filename_in, filename_out, f_learning_set, method, verbose=False):
    setup_classifiers(f_learning_set, method, verbose)
    nb = 0
    with open(filename_in, 'r') as fd_in, open(filename_out, 'w+') as fd_out:
        for line in fd_in.readlines():
            line = re.sub('\s\s+', ' ', line)
            m = re.search('(\<ACTE.+/ACTE\>)', line)
            if m is not None:
                magic = Magic(m.string[m.start(1):m.end(1)], method='text', verbose=verbose)
                magic.run()
                fd_out.write(magic.tostring())
                nb += 1
            else:
                fd_out.write(line)
            fd_out.write("\n")
    print('{} act(s) tagged into {}'.format(nb, filename_out))


def usage():
    print('[args] [filename_in] [filename_out]')
    print('filename_in must be in XML format')
    print('\t-e : extract learning set from filename_in into filename_out')
    print('\t-t : tag acts in filename_in into filename_out')
    print('\t-N : use naive bayes classifier method')
    print('\t-S : use linear SVC method')
    print('\t-v : verbose mode')
    print('\t-l [filename] : when tagging, use it to specify the file which contains learning set')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hetNSvl:', ['help', 'extract', 'tag', 'verbose', 'learning_set=', 'naivebayes', 'linearSVC'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    f_in = None
    f_out = None
    f_learning_set = None
    verbose = False
    extract = False
    tag = False
    method = cst._METHOD_CLASSIFY

    for opt, arg in opts:
        if opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-e', '--extract'):
            extract = True
        elif opt in ('-t', '--tag'):
            tag = True
        elif opt in ('-l', '-learning_set'):
            f_learning_set = arg
        elif opt in ('-N', '--naiebayes'):
            method = 'naive_bayes'
        elif opt in ('-S', '--SVC'):
            method = 'linearSVC'
        else:
            assert False, 'unhandled option'

    if len(args) != 2 :
        print('Take exactly two arguments')
        usage()
        sys.exit()
    f_in = args[0]
    f_out = args[1]

    if extract and tag :
        print('can\'t extract and tag at the same time')
        usage()
        sys.exit()

    logging.basicConfig(filename=cst._LOG_FILE, level=logging.INFO, filemode='w')
    if extract :
        extract_train_acte(f_in, f_out)
    elif tag :
        if f_learning_set is None :
            print('No learning set file specified')
            usage()
            sys.exit()

        tag_multiple_actes(f_in, f_out, f_learning_set, method=method, verbose=verbose)


if __name__ == '__main__':
    main(sys.argv[1:])
