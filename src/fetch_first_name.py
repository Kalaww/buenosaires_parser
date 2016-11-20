#!/usr/bin/python
import urllib2
import database
import utils
import re
import xml.etree.ElementTree as ET

urls = [
    "http://www.behindthename.com/names/usage/spanish",
    "http://www.behindthename.com/names/usage/spanish/2",
    "http://www.behindthename.com/names/usage/spanish/3",
    "http://www.behindthename.com/names/usage/spanish/4"
]

filename = "../data/prenoms.txt"

prenoms = []


def add_prenom(prenoms, prenom):
    prenom = utils.strip_accents(prenom)
    if prenom not in prenoms:
        prenoms.append(prenom)

def save_prenoms(filename, prenoms):
    with open(filename, 'w') as fd:
        for prenom in prenoms:
            fd.write(prenom.encode("utf-8")+"\n")

def get_prenoms(filename, prenoms):
    with open(filename, 'w+') as fd:
        for line in fd.readlines():
            add_prenom(prenoms, line)

def add_database_prenoms(prenoms):
    for prenom in database.get_prenoms(lower_case=True):
        add_prenom(prenoms, prenom)

def add_urls_prenoms(prenoms, urls):
    for url in urls:
        f = urllib2.urlopen(url)
        text = f.read()
        for match in re.finditer(r'<a .*? href="/name/.+?">(.*?)</a>', text):
            print unicode(match.group(1))


# get_prenoms(filename, prenoms)
# add_database_prenoms(prenoms)
# save_prenoms(filename, prenoms)
#
# for p in prenoms[:10]:
#     print(p)

add_urls_prenoms(prenoms, urls)
