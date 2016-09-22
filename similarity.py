# coding: utf8
import os, sys
reload(sys)
sys.setdefaultencoding('utf8')

from nltk.corpus import stopwords
from string import punctuation
#sklearn Package als Ergänzung zum NLTK. Dieses Paket bietet die Möglichkeit tf-idf uz berechnen.
from sklearn.feature_extraction.text import TfidfVectorizer

stopwords = set(stopwords.words('german') + list(punctuation))

#vect = TfidfVectorizer(min_df=1, stop_words=set(stopwords))
vect = TfidfVectorizer(min_df=1)
f1 = open("automatic_summary_02.txt", "r")
f2 = open("reference_summary_flo.txt", "r")
automatic_summary = f1.read()
reference_summary = f2.read()


#Total Frequency und Inverse Document Frequencey Berechnung beider Inhaltsangaben
#tfidf = vect.fit_transform(["Das ist ein schöner Ball.","Das ist ein hässliches Haus."])
tfidf = vect.fit_transform([automatic_summary,reference_summary])

#Kosinusberechnung
cosine=(tfidf * tfidf.T).A
print cosine