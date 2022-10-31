import numpy as np
import csv


# This file contains the functions to perform a weighted and ordinary Levenshtein distance calculator between two words
# Luuk Suurmeijer 21-03-2019

"""

Version 2: Weighted Levenshtein Algorithm. This version of the levenshtein adds weights to the costs of the operations based on 2 CSV files that are passed as arguments.
		   No backtraces yet
Note: The costs of insertion and deletion are the same, because differing it would imply you have knowledge some ancestral state.
	  For example DE: rechnung NL: rekening

using log probabilities because:
 1: faster
 2: Underflow
 3: I can keep adding, so stays closer to the baseline levenshtein algorithm
Means we are now taking maxima rather than minima

Initially: All zeros except first row and column. Those are the cumulative cost of inserting the characters of that 1 by 1.

	   		   v  		  a  		 d  		3  		   r 			<word1
  [[0.         2.30258509 3.5065579  5.80914299 6.16581793 8.46840303]
f  [2.30258509 0.         0.         0.         0.         0.        ]
a  [3.5065579  0.         0.         0.         0.         0.        ]
t  [5.80914299 0.         0.         0.         0.         0.        ]
3  [6.16581793 0.         0.         0.         0.         0.        ]
r  [8.46840303 0.         0.         0.         0.         0.        ]]

^word2

End: All the cells are filled in and the cost is at the bottom right. 
	 In every cell, the minimum of the left corner is taken 
     and the cost of the corresponding operation is added.

			   v		  a			 d			3		   r
  [[0.         2.30258509 3.5065579  5.80914299 6.16581793 8.46840303]
f  [2.30258509 0.05129329 2.35387839 3.86323284 6.16581793 6.59660085]
a  [3.5065579  2.35387839 0.05129329 1.2552661  2.4592389  3.66321171]
t  [5.80914299 3.86323284 1.2552661  0.10258659 2.40517168 2.89002182]
3  [6.16581793 6.16581793 2.4592389  2.40517168 0.10258659 0.45926153]
r  [8.46840303 6.59660085 3.66321171 2.89002182 0.45926153 0.10258659]]


"""
def levenshtein_weighted(word1, word2, substitution, deletion):
	cols = len(word1)+1 #word1 is on the horizontal (corresponds to columns)
	rows = len(word2)+1 #word2 is on the vertical (corresponds to rows)
	distances = np.zeros((rows, cols))

	#initializing
	#set first row to the cumulative cost of the insertion of every character of word2
	for x in range(1, distances.shape[0]):
		distances[x, 0] = distances[x-1, 0] + deletion[word2[x-1]]
	#set first row to the cumulative cost of the insertion of every character of word1
	for y in range(1, distances.shape[1]):
		distances[0, y] = distances[0, y-1] + deletion[word1[y-1]]

	#recurring step
	for row in range(1, distances.shape[0]):
		for col in range(1, distances.shape[1]):
			if word1[col-1] == word2[row-1]: #if the characters are the same (ie, no operation required)
				distances[row, col] = distances[row-1, col-1]
			else:
				distances[row, col] = min( #otherwise, take the minimum of the left upper adjacent cells + the cost of the operation
										distances[row-1, col] + deletion[word1[col-1]], # deletion
										distances[row, col-1] + deletion[word2[row-1]], # insertion
										distances[row-1, col-1] + substitution[ frozenset([word1[col-1], word2[row-1]]) ]  # substitution
										)
					
				
	return distances[rows-1, cols-1]

"""
Version 1: Baseline levenshtein algorithms where every operation has a cost of 1.

Initially:
	    t  e  s  t  s <word1
   [[0. 1. 2. 3. 4. 5.]
t   [1. 0. 0. 0. 0. 0.]
e   [2. 0. 0. 0. 0. 0.]
x   [3. 0. 0. 0. 0. 0.]
t   [4. 0. 0. 0. 0. 0.]]
^word2

End:
        t  e  s  t  s
   [[0. 1. 2. 3. 4. 5.]
t   [1. 0. 1. 2. 3. 4.]
e   [2. 1. 0. 1. 2. 3.]
x   [3. 2. 1. 1. 2. 3.]
t   [4. 3. 2. 2. 1. 2.]]

The levenshtein distance is then the value on the bottom right corner (2)
"""
def levenshtein(word1, word2):
	rows = len(word2)+1 #word2 is on the vertical (corresponds to rows)
	cols = len(word1)+1 #word1 is on the horizontal (corresponds to columns)
	distances = np.zeros((rows, cols))
	#set first row to 1 - string length of first string
	for x in range(distances.shape[0]):
		distances[x, 0] = x
	#set first column to 1 - string length of second string
	for y in range(distances.shape[1]):
		distances[0, y] = y

	for row in range(1, distances.shape[0]):
		for col in range(1, distances.shape[1]):
			if word1[col-1] == word2[row-1]: #if the characters are the same (ie, no operation required)
				distances[row, col] = distances[row-1, col-1]
			else:
				distances[row, col] = min( #otherwise, take the minimum of the left upper adjacent cells + the cost of the operation
										distances[row-1, col]+1, # deletion
										distances[row, col-1]+1, # insertion
										distances[row-1, col-1]+1  # substitution
										)
					
				
	return distances[rows-1, cols-1]
