from HistoricalLM_dev import HLM
from levenshtein2 import levenshtein_weighted
import sys
import csv
from tqdm import tqdm
import numpy as np
from itertools import combinations

"""
Pre-process an AJSP datafile such that it can be read by fast_align.
"""

#provide datafile
datafile = sys.argv[1]

with open(f"parameters/phonetic_substitution.csv", mode='r') as f:
	reader = csv.reader(f)
#keys are frozensets as the order of the sounds does not matter
	sub = {frozenset([row[0], row[1]]) : abs(np.log(float(row[2]))) for row in reader}

with open(f"parameters/phonetic_deletion.csv", mode='r') as f:
	reader = csv.reader(f)
	del_ins = {row[0] : abs(np.log(float(row[1]))) for row in reader}


#make an HLM for the datafile
model = HLM(f"AJSP_1801/{datafile}", sub, del_ins, 3.0)
print(f"\n{len(model.languages)}")


combinations = [(lang1, lang2) for lang1, lang2 in tqdm(list(combinations(model.languages, 2))) if np.average(model.edits(lang1, lang2, False)) < model.threshold]

#in the list of tuples of all unique combinations of langauges, treat languagetuples[0] as source and languagetuples[1] as target
j = 0
for lang1, lang2 in tqdm(combinations, desc="Generating pairs"):
	for i in range(40): #constant length of the wordlists
		try:
			word1 = model.wordlists[lang1][i]
			word2 = model.wordlists[lang2][i]
			#only train on the wordpairs that exist (not None) and can be reasonably expected to be cognates
			if (word1 and word2) and levenshtein_weighted(word1, word2, sub, del_ins) < model.threshold:
				print(f"{' '.join(model.wordlists[lang1][i])} ||| {' '.join(model.wordlists[lang2][i])}")
				j += 1
		except IndexError: #cant figure this out
			pass
