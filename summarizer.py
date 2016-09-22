# coding: utf8
import os, sys
reload(sys)
sys.setdefaultencoding('utf8')

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest

class SimpleSummarizer:
	def __init__(self, min_cut=0.2, max_cut=0.8):
		#Initialisierung des text summarizer.
		#Wörter mit einem Häufigkeitswert von weniger oder mehr als min_cut oder max_cut werden ignoriert.
		#reduce_text reduziert die Länge der Zusammenfassung auf faktor x der Gesamtlänge
		self._min_cut = min_cut
		self._max_cut = max_cut 
		self._stopwords = set(stopwords.words('german') + list(punctuation))
		#print(self._stopwords)

	def _compute_frequencies(self, word_sent):
		# Berechnung der Häufigkeit jedes Wortes
		# Input ist eine Liste von Sätzen, welche bereits tokenized sind.
		# Ouptut ist ein Dictionary mit der Anzahl des jeweiligen wortes.
		freq = defaultdict(int)
		for s in word_sent:
			for word in s:
				if word not in self._stopwords:
					freq[word] += 1
	
		# Häufigkeitsnormalisierung und Filterung
		m = float(max(freq.values()))
		for w in freq.keys():
			freq[w] = freq[w]/m
			if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
				del freq[w]
		return freq

	
	
	def summarize(self, text, n):
		#Rückgabe einer liste von n Sätzen, welche die Textzusammenfassung repräsentieren

		sents = sent_tokenize(text)
		assert n <= len(sents)
		word_sent = [word_tokenize(s.lower()) for s in sents]
		self._freq = self._compute_frequencies(word_sent)
		ranking = defaultdict(int)
		for i,sent in enumerate(word_sent):
			for w in sent:
				if w in self._freq:
					ranking[i] += self._freq[w]
					#print(self._freq[w])
		
		sents_idx = self._rank(ranking, n)
		
		return [sents[j] for j in sents_idx]

	def _rank(self, ranking, n):
		#Rückgabe der ersten n Sätze mit dem höchsten Ranking
		return nlargest(n, ranking, key=ranking.get)

	def summary_size(self, text, reduce_text):
		size = len(sent_tokenize(text)) * reduce_text
		return int(round(size))


	def reorder_sentences( self, summary, input ):
		summary.sort( lambda s1, s2:
			input.find(s1) - input.find(s2) )
		return summary


ss = SimpleSummarizer()
f = open('Artikel.txt', 'r')
input = f.read()

number_of_sentences = ss.summary_size(input, 0.15)
#Ausgabe der Sätze

summary = ss.reorder_sentences(summary, input)
for s in summary:
	print(s)



#for s in ss.summarize(input, number_of_sentences):
	#print('* ' + s)