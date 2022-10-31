import numpy as np # used in levenshtein
import re # pre-processing AJSP files
import csv # reading parameter files
from levenshtein2 import levenshtein_weighted, levenshtein
from lingpy.algorithm import squareform, neighbor #for inferring phylogenetic tree
from ete3 import Tree #visualizing trees
from random import random
from itertools import combinations
from collections import defaultdict, OrderedDict
from tqdm import tqdm
import sys
class HLM:
	"""
	Version 2: Edit distance based on subsitution matrix passed as an argument.

	Class that instantiates what I will informally call a "Historical language model".
	It takes a set of languages and their Swadesh lists in AJSP text format, a subsitution matrix, a insertion/deletion matrix
	and some cognate threshold as a floating point value.
	It can generate a phylogenetic tree based on the average levenshtein distances between the words of the languages
	The following functions are crafted by hand:
		- Pre-processing data
		- Calculating levenshtein distance between words
		- Calculating average levenshtein distance between languages
	The following is done using off the shelf packages:
		- Inferring phylogenetic tree (LingPy)
		- Visualizing tree (ETE)

	Observations so far:
		- Levenshtein is way above chance
		- Weighted levenshtein with phonetic parameters does not perform that much better than expected
	"""

#TODO: NORMALIZE LEVENSHTEIN DISTANCES

	def __init__(self, datafile, sub, del_ins, threshold):
		self.characterlist = [item.strip('\n') for item in open(datafile, 'r').readlines()[43:84]] #lines 43-84 are always the characters in AJSP text format
		self.wordlists = self.preprocessdata(datafile) # data
		self.languages = list(self.wordlists.keys()) # language tags
		self.sub = sub #substitution matrix
		self.del_ins = del_ins #deletion/insertion matrix
		self.threshold = float(threshold) #cognate threshold


	"""
	Pre-processes data in AJSP text format
	Datastructure of self.wordlists is now a dictionary of languages to wordlists
	Where the WORDLIST is a list of TRANSLATIONS
	{LATVIAN : [es, tu, ...], LITHUANIAN : [aS, to, ...], ...}
   	   ^lang	^wordlist        
	"""
	def preprocessdata(self, rawtext):
		lang_tags = []
		wordlists_all = []
		wordlist = []
		with open(rawtext, "r") as f:
			for line in tqdm(f, desc="Reading"): #opted to not go for a list comprehension here for readability
				match_tag = re.search(r'(\w+)(?=\{.+\})', line) #regex for language name
				match_word = re.search(r'(\w+)\t(\%?(\w|~|$)+)', line) #regex for the structure of each word and concept
				if match_tag: #if you encounter a new language, append all the words so far and start a new list
					lang_tags.append(match_tag.group(0))
					if wordlist: # wordlist is empty at first
						wordlists_all.append(wordlist)
						wordlist = []
				if match_word:
				#remove diacritics, encode missing data as None, treat guaranteed loanwords (%) as missing data
					if match_word.group(2) == ' ' or match_word.group(2) == 'XXX': #TODO:or '%' in match_word.group(2): #group(2) of word_tag is the translation of the concept
						wordlist.append(None)
					else:
						wordlist.append(''.join([i for i in match_word.group(2) if i in self.characterlist])) #remove diacritics
			wordlists_all.append(wordlist) # append last wordlist in memory
		return dict(zip(lang_tags, wordlists_all)) # return a dictionary with languages as keys and wordlists as values
	


	"""
	Returns a list with weighted edit distance between words with the same meaning of two languages as items
	Uses the function 'levenshtein_weighted()' from levenshtein2.py
	"""

	def edits(self, language1, language2, weighted):
		#some lists have 40 entries, some 100. I want to compare as much data as possible
		#in the rare case, a list has fewer than 40 entries
		#that is why I have to use min() to determine the range
		l = min(len(self.wordlists[language1]),len(self.wordlists[language2]))

		if weighted:
			#list of levenshtein values between the entries of language1 and language2 if both entries are non-empty
			all_scores = [levenshtein_weighted(self.wordlists[language1][i], self.wordlists[language2][i], self.sub, self.del_ins) 
							for i in range(l)
							if (self.wordlists[language1][i] and self.wordlists[language2][i])] #dont consider missing entries
		else:
			all_scores = [levenshtein(self.wordlists[language1][i], self.wordlists[language2][i]) 
							for i in range(l)
							if (self.wordlists[language1][i] and self.wordlists[language2][i])]

		return [distance for distance in all_scores if distance < self.threshold] #return only those scores that are below the cognate threshold (constant)


	"""
	Calculate the average (weighted) edit distance of each pair of languages and return a dictionary with tuples of languages as keys
	and the average distance between the languages in the tuples as values         
	"""

	def average_edits_all(self, data, weighted=True): #provided data is in the same format as self.wordlists
		lang_distances_all = OrderedDict() #order matters for the phylogenetic inference
		for lang1, lang2 in tqdm(list(combinations(data.keys(), 2)), desc="Calculating distances"):
			#some languages have no data at all, but are still in AJSP, filter before you do any work and tell user
			if not any(data[lang1]) or not any(data[lang2]):
				print(f"No data between {lang1} and {lang2}")
				pass
			else:
				pair_distances = self.edits(lang1, lang2, weighted)
				#calculate average score between lang1 and lang2
				lang_distances_all[(lang1, lang2)] = sum(pair_distances) / len(pair_distances)
	
		return lang_distances_all

	"""
	Generate a phylogenetic tree based on the pairwise average Levenshtein distance and the language names.	

	"""

	def get_tree(self, data):
		distances = squareform(data)
		t = neighbor(distances, self.languages)
		t = Tree(t)

		return t
