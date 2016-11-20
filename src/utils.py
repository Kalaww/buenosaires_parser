import unicodedata

def strip_accents(text):
    return unicodedata.normalize('NFKC', ''.join(c for c in unicodedata.normalize('NFKD', text)
if unicodedata.category(c) != 'Mn'))
