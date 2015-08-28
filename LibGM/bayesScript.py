#from numpy import genfromtxt
import json
import pandas as pd
import csv
import numpy
import re
import os, fnmatch


from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.lgbayesiannetwork import LGBayesianNetwork
from libpgm.pgmlearner import PGMLearner



#text_file = open('paths/"west nile virus".txt', "r")

#lines = text_file.read()
#lines = re.sub('[]', '', lines)

#print lines

## INPUT: Directory path
## OUTPUT: Outputs all files in directory path
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)

## INPUT: filePath name
## OUTPUT: textFile with name of outputTextFile
def cleanText (inputTextFile,outputTextFile):
	with open(inputTextFile, 'r') as infile, open(outputTextFile, 'w') as outfile:
    		data = infile.read()
    		data = data.replace(",", "")
   	 	data = data.replace("]", "")
    		data = data.replace("[", "")	
    		outfile.write(data)
	infile.closed	
	outfile.closed

def bayesNet(textFile):
	cleanText(textFile,'tempOutput.txt')

	## imports textFile into pandas

	try:
		df = pd.read_csv('tempOutput.txt', sep='\s+',dtype='float32',header=None)
	except:
		print 'next file'
		return
	df.fillna(0, inplace=True)
	df.convert_objects(convert_numeric=True)

	## 

	for i, row in df.iterrows():
		print df.ix[0,i]
     		df.ix[0,i] = df.ix[0,i] + str(i)		

	grouped = df.set_index([0], verify_integrity=True)

	df2 = grouped.to_dict()

	print json.dumps(df2, indent=2)	
	
	newDict = []

	for key in df2.keys():
		newDict.append(df2[key])

	
	#print json.dumps(newDict, indent=2)
# instantiate my learner 
	learner = PGMLearner()

# estimate structure
	result = learner.lg_constraint_estimatestruct(newDict)

# output
	return json.dumps(result.E, indent=2)



	

