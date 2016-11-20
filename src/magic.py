# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re

class Magic:

    def __init__(self, str, method='text'):
        self.root = None
        if(method == 'file'):
            self.from_file(str)
        if(method == 'text'):
            self.from_string(str)

    def from_file(self, filename):
        print 'loading file {}'.format(filename)
        self.root = (ET.parse(filename)).getroot()

    def from_string(self, str):
        print 'loading text'
        str = str.encode('utf-8')
        self.root = ET.fromstring(str)

    def tostring(self):
        return ET.tostring(self.root, encoding='utf-8', method='xml')

    def run(self):
        print self.tostring()
        self.check_date()
        print self.tostring()

    def check_date(self):
        print '<date> checking ...'
        date = self.root.find('date')
        if(date is not None):
            print '<date> already done'
            return True
        print '<date> missing, researching potential date'
        text = self.root.text
        if(text is None):
            print '<date> no text to search for date'
            return False

        splitted = re.split('(\d{1,2}-\d{1,2}-\d{4})', text)
        if(len(splitted) != 3):
            print '<date> no date found'
            return False
        self.root.text = splitted[0]
        elem = ET.Element('date')
        elem.text = splitted[1]
        elem.tail = splitted[2]

        self.root._children.insert(0, elem)
        print '<date> found !'
        return True






def extract_actes_from_xml(xml_tree):
    return [acte for acte in xml_tree.getroot().iter("ACTE")]
