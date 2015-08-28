## INPUT: This file will read the CPDB_pathways_genes.txt file
## OUTPUT: Files named by pathway containing gene names

from numpy import genfromtxt
import json
import pandas as pd
import csv
import string
import os, fnmatch

# Finds all probes relating to a particular set of genes



def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)


# make frequency table
freqTable = pd.DataFrame(columns=('Gene1', 'Gene2','Count'))



for textFile in findFiles('boost', '*'):
	print textFile
	boost = pd.read_csv(textFile, sep=',', header=None)
	
	#print "boost is "
	#print boost
	# go rough each row of boost

	for index, row in boost.iterrows():
		#print row
		#print "freqtable is"
		#print freqTable
		#if (row1 is in Gene1 and row2 is in Gene2) or opp:
 			# if row exists in frequency table add 1 to count
		if freqTable[(freqTable.Gene1 == row[2])&(freqTable.Gene2 == row[3])].empty:
		#	print "its empty"
		#	print "row 2 is"
		#	print row[2]
			df = pd.DataFrame([[row[2],row[3],1]], columns = ['Gene1','Gene2','Count'])
		#	print "df is "
		#	print df
			freqTable = freqTable.append(df, ignore_index=True)
			
			#print "freqtable is"
			#print freqTable
		else:	
			#print "been here before"
			freqTable.Count[(freqTable.Gene1 == row[2])&(freqTable.Gene2 == row[3])] += 1
			#print freqTable[(freqTable.Gene1 == row[2])&(freqTable.Gene2 == row[3])]
		freqTable.convert_objects(convert_numeric=True)

#	print freqTable

freqTable.to_csv('FrequencyBoost.csv')

#freqTable.[(freqTable.Gene1 == row[1])&(freqTable.Gene2 == row[2])].count + 1
