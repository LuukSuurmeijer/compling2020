READ ME FOR COMPUTATIONAL LINGUISTICS FINAL PROJECT

This zip file contains the following files and directories:
.
├── HistoricalLM_dev.py	- Class for reading AJSP datafile and performing language relatedness assessment
├── levenshtein2.py		- Contains weighted Levenshtein and base Levenshtein functions
├── preprocessing.py 	- Script to preprocess AJSP data for fast_align
├── gen_trees.py 		- Script to generate plots and trees
├── parameters			- Folder with the training files and the output files of fast_align
│   ├── bantutraining.in
│   ├── phonetic_deletion.csv
│   ├── phonetic_substitution.csv
│   ├── substitutionprob.csv
│   ├── training_all.in
│   └── translationprob.csv
├── AJSP_1801			- Folder with all wordlists used form AJSP
│   ├── austronesian.txt
│   ├── baltic.txt
│   ├── bantu.txt
│   ├── berber.txt
│   ├── germanic.txt
│   ├── listss18_training.txt
│   ├── listss18.txt	- Full dataset
│   ├── romance.txt
│   ├── semitic.txt
│   ├── unrelated.txt
│   ├── uralic.txt
│   ├── uto-aztecan.txt
│   └── westgermanic.txt
├── Output				- Folder with Newick strings for Germanic tree
│   ├── germanic_base_5.nw
│   ├── germanic_custom_5.nw
│   ├── germanic_EM_5.nw
│   ├── germanicgold.nw
│   ├── germanic_random.nw
├── report.pdf	 		- Report
├── README.txt	 		- This readme

The following packages are necesarry to run this project:
- lingpy
- ete3
- numpy
- random
- tqdm
- re
- csv
- matplotlib

In order to get some data with the file "gen_tree.py", specify the two AJSP files in the AJSP_1801 folder you'd like to get data for as commandline arguments (no file ending), as well as a cognate threshold (float). Currently, the file will generate a violinplot, functionality for generating phylogenetic trees is there 
(as per the function in HistoricalLM_dev.py). 
