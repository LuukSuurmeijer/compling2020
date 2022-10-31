import csv
import sys
import numpy as np
from random import random, sample
from itertools import combinations
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
from HistoricalLM_dev import HLM


"""
Generate violinplot for two groups of languages and a random sample from the full dataset.
Commandline arguments: Two AJSP datafiles (no file ending) and a cognate threshold
"""

datafile1, datafile2, cognate_threshold = sys.argv[1:]

#open all files
with open(f"parameters/phonetic_substitution.csv", mode='r') as f:
	reader = csv.reader(f)
	#keys are frozensets as the order of the sounds does not matter
	sub = {frozenset([row[0], row[1]]) : abs(np.log(float(row[2]))) for row in reader}

with open(f"parameters/phonetic_deletion.csv", mode='r') as f:
	reader = csv.reader(f)
	del_ins = {row[0] : abs(np.log(float(row[1]))) for row in reader}

with open(f"parameters/all_translationprob.csv", mode ='r') as f:
	reader = csv.reader(f, delimiter='\t')
	sub_EM = {frozenset([row[0], row[1]]) : abs((float(row[2]))) for row in reader}

with open(f"parameters/all_deletion.csv", mode='r') as f:
	reader = csv.reader(f, delimiter='\t')
	del_ins_EM = {row[1] : abs((float(row[2]))) for row in reader}

#make all the models
related_ger = HLM(f"AJSP_1801/{datafile1}.txt", sub_EM, del_ins_EM, cognate_threshold)
related_ua = HLM(f"AJSP_1801/{datafile2}.txt", sub_EM, del_ins_EM, cognate_threshold)
both = HLM(f"AJSP_1801/listss18.txt", sub_EM, del_ins_EM, cognate_threshold)


#get a list of pairwise scores for each of the three models
related_ger_avg = list(related_ger.average_edits_all(related_ger.wordlists).values())
related_ua_avg = list(related_ua.average_edits_all(related_ua.wordlists).values())

#random sample for the full dataset
sam =sample(list(both.wordlists), 100)
wordlistsnew = {lang : both.wordlists[lang] for lang in sam}
print(f"{wordlistsnew.keys()}\n{len(wordlistsnew)}")
both_avg = list(both.average_edits_all(wordlistsnew).values())

#make a plot
plotdict = {"{datafile1}" : related_ger_avg, "{datafile2}" : related_ua_avg, "Random" : both_avg}
data = (related_ger_avg, related_ua_avg, both_avg)

fig, ax = plt.subplots()

plot = ax.violinplot(data, showmeans=True)
colors = ['springgreen', 'dodgerblue', 'hotpink']
for patch, color in zip(plot['bodies'], colors):
	patch.set_facecolor(color)


ax.get_xaxis().set_tick_params(direction='out')
ax.xaxis.set_ticks_position('bottom')
ax.set_xticks(np.arange(1, len(plotdict.keys()) + 1))
ax.set_xticklabels(plotdict.keys())
ax.set_xlabel('Grouping')
ax.set_ylabel('Pairwise Levenshtein scores')

plt.show()
