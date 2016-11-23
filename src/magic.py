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
        self.check_epoux()
        self.check_epouse()
        self.check_temoins()
        print self.tostring()

    def check_date(self):
        print '<date> checking ...'
        date = self.root.find('date')
        if(date is not None):
            print '<date> already done'
            return True
        print '<date> missing, researching ...'
        text = self.root.text
        if(text is None):
            print '<date> no text to search for date'
            return False
        m = re.search('(\d{1,2}-\d{1,2}-\d{4})', text)
        if(m is None):
            print '<date> not found'
            return False
        self.root.text = m.string[:m.start(0)]
        elem = ET.Element('date')
        elem.text = m.string[m.start(0):m.end(0)]
        elem.tail = m.string[m.end(0):]

        self.root._children.insert(0, elem)
        print '<date> found !'
        return True

    def check_epoux(self):
        print '<epoux> checking ...'
        epoux = self.root.find('epoux')
        if(epoux is not None):
            print '<epoux> already done'
        else:
            print '<epoux> missing, researching ...'
            date = self.root.find('date')
            m = re.match(':(.*), con', date.tail)
            if(m is None):
                print '<epoux> not found'
            else:
                date.tail = m.string[:m.start(1)]
                elem = ET.Element('epoux')
                elem.text = m.string[m.start(1):m.end(1)]
                elem.tail = m.string[m.end(1):]
                self.root._children.insert(1, elem)
                print '<epoux> found !'

    def check_epouse(self):
        print '<epouse> checking ...'
        epouse = self.root.find('epouse')
        if(epouse is not None):
            print '<epouse> already done'
        else:
            print '<epouse> missing, researching ...'
            epoux = self.root.find('epoux')
            m = re.match(', con (.*)\. .s\.:', epoux.tail)
            if(m is None):
                print '<epouse> not found'
            else:
                epoux.tail = m.string[:m.start(1)]
                elem = ET.Element('epouse')
                elem.text = m.string[m.start(1):m.end(1)]
                elem.tail = m.string[m.end(1):]
                self.root._children.insert(2, elem)
                print '<epouse> found !'

    def check_temoins(self):
        print '<temoins> checking ...'
        temoins = self.root.find('temoins')
        if(temoins is not None):
            print '<temoins> already done'
        else:
            print '<temoins> missing, researching ...'
            epouse = self.root.find('epouse')
            m = re.match('\. .s\.: (.+?(?<!Dn|Da)\.)', epouse.tail)
            if(m is None):
                print '<temoins> not found'
            else:
                epouse.tail = m.string[:m.start(1)]
                elem = ET.Element('temoins')
                elem.text = m.string[m.start(1):m.end(1)]
                elem.tail = m.string[m.end(1):]
                self.root._children.insert(3, elem)
                print '<temoins> found !'
                temoins = elem
        self.check_temoin(temoins)

    def check_temoin(self, temoins):
            if(current is None):
                more = False
            else:
                temoins.append(current)

    def search_temoin(self, node):
        if(node.tag == 'temoins'):
            str = node.text
        else:
            str = node.tail
        m = re.match('.*?((Da\.|Dn\.).+?)(y Da\.|y Dn\.|\.)', str)
        if(m is None):
            print '<temoin> no more found'
            return None
        elem = ET.Element('temoin')
        elem.text = m.string[m.start(1):m.end(1)]
        elem.tail = m.string[m.end(1):]
        if(node.tag == 'temoins'):
            node.text = m.string[:m.start(1)]
        else:
            node.tail = m.string[:m.start(1)]
        print '<temoin> one more found'
        return elem




def extract_actes_from_xml(xml_tree):
    return [acte for acte in xml_tree.getroot().iter("ACTE")]
