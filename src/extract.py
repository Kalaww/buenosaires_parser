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

    def get_noms(self):
        return self.get_tag_contents('nom')

    def get_prenoms(self):
        return self.get_tag_contents('prenom')

    def get_tag_contents(self, tag):
        contents = []
        for acte in self.actes:
            for item in self.recursive_search(acte, tag):
                contents.append(item.strip())
        print('{} {} found'.format(len(contents), tag))
        return contents

    def recursive_search(self, root, tag):
        texts = []
        for child in root:
            if(child.tag == tag):
                texts.append(child.text)
            else:
                texts = texts + self.recursive_search(child, tag)
        return texts
