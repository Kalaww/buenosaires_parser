import re
import codecs
import xml.etree.ElementTree as ET

def extract_train_acte(filename_in, filename_out):
    with open(filename_in, 'r') as fd_in, open(filename_out, 'w+') as fd_out:
        for line in fd_in.readlines():
            if('<nom>' in line):
                fd_out.write(line)

class Extractor:

    def __init__(self, filename):
        self.actes = []
        with codecs.open(filename, 'r', encoding='utf-8') as fd:
            for line in fd.readlines():
                line = re.sub(r'\s+', ' ', line).strip()
                self.actes.append(ET.fromstring(line))

    def extract_tag(self, tag, filename=None):
        contents = []
        fd = None
        if(filename is not None):
            fd = open(filename, 'w')

        for acte in self.actes:
            for item in self.recursive_search(acte, tag):
                contents.append(item)
                if(fd is not None):
                    fd.write(item)
                    fd.write('\n')
        print('{} {} found'.format(len(contents), tag))
        return contents

    def recursive_search(self, root, tag):
        texts = []
        for i in range(0, len(root)):
            if(root[i].tag == tag):
                before = None
                position = i -1
                while before is None:
                    if(position < -1):
                        break
                    if(position == -1):
                        before = last_word(root.text)
                    else:
                        before = last_word(root[i].tail)
                        if(before is None):
                            before = last_word(root[i].text)
                    position -= 1

                after = None
                position = i
                while after is None:
                    if(position > len(root)):
                        break
                    if(position == len(root)):
                        after = first_word(root.tail)
                    elif(position == i):
                        after = first_word(root[i].tail)
                    else:
                        after = first_word(root[position].text)
                        if(after is None):
                            after = first_word(root[position].tail)
                    position += 1
                if(before is None):
                    before = ''
                if(after is None):
                    after = ''
                texts.append((root[i].text, before, after))
            else:
                texts = texts + self.recursive_search(root[i], tag)
        return texts

def last_word(str):
    if(str is None):
        return None
    split = str.rsplit(None, 1)
    if(len(split) > 0):
        return split[-1]
    return None

def first_word(str):
    if(str is None):
        return None
    split = str.rsplit(None, 1)
    if(len(split) > 0):
        return split[0]
    return None
