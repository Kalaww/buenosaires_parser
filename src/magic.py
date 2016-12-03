# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import logging

class Magic:

    regex = {
        'date': ('((\d{1,2}-\d{1,2}-)?\d{4}) ?:', 1),
        'epoux': ('(.*: ?|\d+\) )(.*?)(,)? con ', 2)
    }

    def __init__(self, str, method='text'):
        self.root = None
        self._stop = False
        self._original_text = str
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
        return ET.tostring(self.root, encoding='unicode', method='xml')

    def run(self):
        if(self._stop):
            return
        # logging.debug(self.tostring())
        self.check_date()
        self.check_epoux()
        # self.check_epouse()
        # self.check_temoins()
        # logging.debug(self.tostring())

    def check_pattern(self, root, tag, before=[]):
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

        m = re.search(self.regex[tag][0], text)

        if(m is None):
            return False

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
        self.check_pattern(self.root, 'date')

    def check_epoux(self):
        return self.check_pattern(self.root, 'epoux', ['date'])


    # def check_date(self):
    #     logging.debug('<date> checking ...')
    #     date = self.root.find('date')
    #     if(date is not None):
    #         logging.debug('<date> already done')
    #         return True
    #
    #     logging.debug('<date> missing, researching ...')
    #     text = self.root.text
    #     if(text is None):
    #         logging.debug('<date> no text to search for date')
    #         return False
    #
    #     m = re.search('((\d{1,2}-\d{1,2}-)?\d{4}) ?:', text)
    #     if(m is None):
    #         logging.debug('<date> not found')
    #         return False
    #     self.root.text = m.string[:m.start(1)]
    #     elem = ET.Element('date')
    #     elem.text = m.string[m.start(1):m.end(1)]
    #     elem.tail = m.string[m.end(1):]
    #
    #     self.root.insert(0, elem)
    #     logging.debug('<date> found !')
    #     return True
    #
    # def check_epoux(self):
    #     logging.debug('<epoux> checking ...')
    #     epoux = self.root.find('epoux')
    #
    #     if(epoux is not None):
    #         logging.debug('<epoux> already done')
    #     else:
    #         logging.debug('<epoux> missing, researching ...')
    #         date = self.root.find('date')
    #         if(date is None):
    #             text = self.root.text
    #         else:
    #             text = date.tail
    #
    #         m = re.match('.*: ?(.*?)(,)? con ', text)
    #         if(m is None):
    #             logging.debug('<epoux> not found')
    #         else:
    #             if(date is None):
    #                 self.root.text = m.string[:m.start(1)]
    #             else:
    #                 date.tail = m.string[:m.start(1)]
    #             elem = ET.Element('epoux')
    #             elem.text = m.string[m.start(1):m.end(1)]
    #             elem.tail = m.string[m.end(1):]
    #             self.root.insert(1, elem)
    #             logging.debug('<epoux> found !')



    # def check_epouse(self):
    #     logging.debug('<epouse> checking ...')
    #     epouse = self.root.find('epouse')
    #
    #     if(epouse is not None):
    #         logging.debug('<epouse> already done')
    #     else:
    #         logging.debug('<epouse> missing, researching ...')
    #         epoux = self.root.find('epoux')
    #         if(epoux is None):
    #             date = self.root.find('date')
    #             if(date is None):
    #                 text = self.root.text
    #             else:
    #                 text = date.tail
    #         else:
    #             text = epoux.tail
    #         m = re.match(', con (.*)\. .s\.:', text)
    #         if(m is None):
    #             logging.debug('<epouse> not found')
    #         else:
    #             if(epoux is None):
    #                 date = self.root.find('date')
    #             epoux.tail = m.string[:m.start(1)]
    #             elem = ET.Element('epouse')
    #             elem.text = m.string[m.start(1):m.end(1)]
    #             elem.tail = m.string[m.end(1):]
    #             self.root._children.insert(2, elem)
    #             logging.debug('<epouse> found !')
    #
    # def check_temoins(self):
    #     logging.debug('<temoins> checking ...')
    #     temoins = self.root.find('temoins')
    #     if(temoins is not None):
    #         logging.debug('<temoins> already done')
    #     else:
    #         logging.debug('<temoins> missing, researching ...')
    #         epouse = self.root.find('epouse')
    #         m = re.match('\. .s\.: (.+?(?<!Dn|Da)\.)', epouse.tail)
    #         if(m is None):
    #             logging.debug('<temoins> not found')
    #         else:
    #             epouse.tail = m.string[:m.start(1)]
    #             elem = ET.Element('temoins')
    #             elem.text = m.string[m.start(1):m.end(1)]
    #             elem.tail = m.string[m.end(1):]
    #             self.root._children.insert(3, elem)
    #             logging.debug('<temoins> found !')
    #             temoins = elem
    #     self.check_temoin(temoins)
    #
    # def check_temoin(self, temoins):
    #     if(current is None):
    #         more = False
    #     else:
    #         temoins.append(current)
    #     m = re.match('.*?((Da\.|Dn\.).+?)(y Da\.|y Dn\.|\.)', str)
    #     if(m is None):
    #         logging.debug('<temoin> no more found')
    #         return None
    #     elem = ET.Element('temoin')
    #     elem.text = m.string[m.start(1):m.end(1)]
    #     elem.tail = m.string[m.end(1):]
    #     if(node.tag == 'temoins'):
    #         node.text = m.string[:m.start(1)]
    #     else:
    #         node.tail = m.string[:m.start(1)]
    #     logging.debug('<temoin> one more found')
    #     return elem




def extract_actes_from_xml(xml_tree):
    return [acte for acte in xml_tree.getroot().iter("ACTE")]
