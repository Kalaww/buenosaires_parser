
import xml.etree.ElementTree as ET
import re
import logging


from src.classifier import best_classify

class Magic:

    regex = {
        'date': ( '((\d{1,2}-\d{1,2}-)?\d{4}) ?:', 1),
        'epoux': ('(.*: ?|\d+\) )(.*?)(,)? con ', 2),
        'epouse': (' con (.+?)\.(?<!(Da.|Dn.))', 1),
        'temoins': ('Ts\.: (.+?)((?<!Dn|Da)|, \(f)\.', 1),
        'naissance-lieu': ('natural(es)? del? (.+?)(,|$)', 2),
        'pere/mere': ('hij(o|a)( leg.tim(o|a)| natural)? del? (.+)(?<!,),? y de (.+?)(,|$)', (4, 5))
    }

    def __init__(self, str, method='text', verbose=False):
        self.root = None
        self._stop = False
        self._original_text = str
        self.verbose = verbose
        if(method == 'file'):
            self.from_file(str)
        if(method == 'text'):
            self.from_string(str)

    def from_file(self, filename):
        logging.debug('loading file %s', 'filename')
        self.root = (ET.parse(filename)).getroot()

    def from_string(self, str):
        logging.debug('loading text')
        str = str.encode('utf-8')
        try:
            self.root = ET.fromstring(str)
        except:
            logging.error("impossible de lire l'XML suivant: %s", str)
            self._stop = True

    def tostring(self):
        if(self._stop):
            return self._original_text
        str = ET.tostring(self.root, encoding='unicode', method='html')
        str = re.sub('\\&lt;', '<', str)
        return re.sub('\\&gt;', '>', str)

    def run(self):
        if(self._stop):
            return

        self.check_date()
        self.check_epoux()
        self.check_epouse()
        self.check_temoins()

        persons = []
        persons += self.root.findall('./epoux')
        persons += self.root.findall('./epouse')
        persons += self.root.findall('.//pere')
        persons += self.root.findall('.//mere')
        persons += self.root.findall('.//temoin')

        for person in persons:
            person_words(person)

    def check_pattern(self, root, tag, before=[], multiple=False):
        if(root.find(tag) is not None):
            return True

        target = root
        position = 0
        for tag_str in before:
            found = False
            tmp = 0
            for child in root:
                tmp += 1
                if(child.tag == tag_str):
                    target = child
                    position = tmp
                    found = True
                    break
            if(found):
                break

        if(target is root):
            text = target.text
        else:
            text = target.tail

        if text is None:
            return False

        m = re.search(self.regex[tag][0], text)

        if(m is None):
            return False

        if(multiple):
            nb_tag = len(self.regex[tag][1])
            tags = tag.split('/')

            for index in range(0,nb_tag):
                i = self.regex[tag][1][index]
                if(index == 0):
                    before = m.string[:m.start(i)]
                else:
                    before = m.string[m.end(self.regex[tag][1][index-1]):m.start(i)]
                if(target is root):
                    target.text = before
                else:
                    target.tail = before

                elem = ET.Element(tags[index])
                elem.text = m.string[m.start(i):m.end(i)]
                elem.tail = m.string[m.end(i):]

                root.insert(position, elem)

                position += 1
                target = elem
        else:
            i = self.regex[tag][1]
            if(target is root):
                target.text = m.string[:m.start(i)]
            else:
                target.tail = m.string[:m.start(i)]

            elem = ET.Element(tag)
            elem.text = m.string[m.start(i):m.end(i)]
            elem.tail = m.string[m.end(i):]

            root.insert(position, elem)
        return True

    def check_date(self):
        return self.check_pattern(self.root, 'date')

    def check_epoux(self):
        self.check_pattern(self.root, 'epoux', ['date'])

        epoux = self.root.find('epoux')
        if(epoux is None):
            return

        self.check_pattern(epoux, 'naissance-lieu')
        self.check_pattern(epoux, 'pere/mere', ['naissance-lieu'], multiple=True)

    def check_epouse(self):
        self.check_pattern(self.root, 'epouse', ['epoux', 'date'])

        epouse = self.root.find('epouse')
        if(epouse is None):
            return

        self.check_pattern(epouse, 'naissance-lieu')
        self.check_pattern(epouse, 'pere/mere', ['naissance-lieu'], multiple=True)

    def check_temoins(self):
        self.check_pattern(self.root, 'temoins', ['epouse', 'epoux', 'date'])

        temoins = self.root.find('temoins')
        if(temoins is None):
            return

        if temoins.text is None:
            return
        splitted, str = self.split_temoins(temoins.text)

        i = 0
        size = len(splitted)
        while True:
            if(i >= size):
                break
            elem = ET.Element('temoin')
            elem.text = splitted[i]
            i += 1

            if(i < size):
                elem.tail = splitted[i]
                i += 1
            temoins.append(elem)
        temoins.text = ''

    def split_temoins(self, str):
        splitted = []
        while True:
            y = str.find(', ')
            yy = str.find(', y ')

            if(y == -1 and yy == -1):
                break

            if(yy == y):
                min = yy
                max = min + len(', y ')
            else:
                min = y
                max = min + len(', ')

            splitted.append(str[:min])
            splitted.append(str[min:max])
            str = str[max:]
        if(len(str) > 0):
            splitted.append(str)
        return splitted, str


def extract_actes_from_xml(xml_tree):
    return [acte for acte in xml_tree.getroot().iter("ACTE")]

def person_words(node):
    regex_split = '(.+?)((\W+)|$)'
    words = []
    if node.text is not None:
        for m in re.finditer(regex_split, node.text):
            words.append((m.group(1), 'other', m.group(3)))
        words = setup_features_words(words)
        if len(words) > 0 and len(node) > 0 :
            words[-1][0]['after_tag'] = node[0].tag
        node.text = classify(words)

    for i in range(0, len(node)):
        words = []
        if node[i].tail is not None:
            for m in re.finditer(regex_split, node[i].tail):
                words.append((m.group(1), 'other', m.group(3)))
            words = setup_features_words(words)
            if len(words) > 0 and i+1 < len(node):
                words[-1][0]['after_tag'] = node[i+1].tag
            node[i].tail = classify(words)

def classify(words):
    for tmp in range(0, 2):
        for i in range(0, len(words)):
            if words[i][1] != 'other':
                continue
            predicted = best_classify(words[i][0])
            if predicted is not 'other':
                words[i] = (words[i][0], predicted, words[i][2])
                if i > 0:
                    features = {}
                    for k, v in words[i - 1][0].items():
                        features[k] = v
                    features['after_tag'] = words[i][1]
                    words[i - 1] = (features, words[i - 1][1], words[i-1][2])
                if i < len(words) - 1:
                    features = {}
                    for k, v in words[i + 1][0].items():
                        features[k] = v
                    features['before_tag'] = words[i][1]
                    words[i + 1] = (features, words[i + 1][1], words[i+1][2])

    str = ''
    for features, tag, next in words:
        if tag != 'other' :
            str += '<{}>{}</{}>'.format(tag, features['word'], tag)
        else:
            str += features['word']
        if next is not None:
            str += next
    return str

def setup_features_words(words):
    results = []
    for i, (word, tag, next) in enumerate(words):
        before = ''
        before_tag = 'other'
        if i > 0:
            before = words[i - 1][0]
            before_tag = words[i - 1][1]
        after = ''
        after_tag = 'other'
        if i < len(words) - 1:
            after = words[i + 1][0]
            after_tag = words[i + 1][1]
        results.append(
            ({
                 'word': word,
                 'before': before,
                 'after': after,
                 'before_tag': before_tag,
                 'after_tag': after_tag
             }, tag, next)
        )
    return results
