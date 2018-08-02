import pandas as pd
import numpy as np 
import string
import random

import nltk
from nltk.corpus import brown
from nltk.corpus import reuters

from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

from nltk.corpus import stopwords

#from nltk.stem.porter import PorterStemmer
#from nltk.stem import SnowballStemmer
import math
#from textblob import TextBlob as tb
from nltk.corpus import *

import re
from collections import Counter
import webbrowser
exclude = set(string.punctuation)
alldocslist = []
dir="documents"
reuter=PlaintextCorpusReader(dir,'.*',encoding="ISO-8859-1");

for index, i in  enumerate(reuter.fileids()):
    text = reuter.raw(fileids=[i])
    text = ''.join(ch for ch in text if ch not in exclude)
    alldocslist.append(text)

plot_data = [[]] * len(alldocslist)

for doc in alldocslist:
    text = doc
    tokentext = word_tokenize(text)
    plot_data[index].append(tokentext)

for x in range(len(reuter.fileids())):
    lowers = [word.lower() for word in plot_data[0][x]]
    plot_data[0][x] = lowers

stop_words = set(stopwords.words('english'))

for x in range(len(reuter.fileids())):
    filtered_sentence = [w for w in plot_data[0][x] if not w in stop_words]
    plot_data[0][x] = filtered_sentence

#snowball_stemmer = SnowballStemmer("english")
#porter_stemmer = PorterStemmer()
l = plot_data[0]
flatten = [item for sublist in l for item in sublist]
words = flatten
wordsunique = set(words)
wordsunique = list(wordsunique)

def tf(word, doc):
    return doc.count(word) / len(doc)

def n_containing(word, doclist):
    return sum(1 for doc in doclist if word in doc)

def idf(word, doclist):
    return math.log(len(doclist) / (0.01 + n_containing(word, doclist)))

def tfidf(word, doc, doclist):
    return (tf(word, doc) * idf(word, doclist))


plottest = plot_data[0][0:len(alldocslist)]

worddic = {}

for doc in plottest:
    for word in wordsunique:
        if word in doc:
            word = str(word)
            index = plottest.index(doc)
            positions = list(np.where(np.array(plottest[index]) == word)[0])
            idfs = tfidf(word,doc,plottest)
            try:
                worddic[word].append([index,positions,idfs])
            except:
                worddic[word] = []
                worddic[word].append([index,positions,idfs])
np.save('worddic_999.npy', worddic)



