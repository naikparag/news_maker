import spacy
from spacy.lang.en.examples import sentences
from spacy import displacy

nlpEngine = spacy.load('en_core_web_sm')

def nlp(title, text):
    titleHTML = performNLP(title)
    textHTML = performNLP(text)
    return titleHTML, textHTML

def performNLP(document):
    result = nlpEngine(document)
    return displacy.render(result, style='ent')