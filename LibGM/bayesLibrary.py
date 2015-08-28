#from numpy import genfromtxt
import json
import pandas as pd
import csv
import numpy
import re
import os, fnmatch
from numpy import *
from math import *

from sklearn.decomposition import PCA

from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.lgbayesiannetwork import LGBayesianNetwork
from libpgm.pgmlearner import PGMLearner
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork


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

# makes repetitions of genes unique by appending row number
def setUnique(df):
	for i, row in df.iterrows():
     		df.ix[i,0] = df.ix[i,0]  +'_' + str(i)	
	return df.set_index([0], verify_integrity=True)

# sets repetitions to there maximum value
def setMax(df):
	return df.groupby([0]).max()

def quantize(number, dataFrame):
	for i, row in dataFrame.iterrows():
		dataFrame.ix[i] = pd.qcut(row,number).labels
	return dataFrame

def DFtoLibpgm(dataFrame):
	df2 = dataFrame.to_dict()
	newDict = []
	for key in df2.keys():
		newDict.append(df2[key])
	return newDict

def bayesNetDiscrete(textFile,quant_no,unique):
	cleanText(textFile,'tempOutput.txt')

	## imports textFile into pandas
	try:
		df = pd.read_csv('tempOutput.txt', sep='\s+',dtype='float64',header=None)
	except:
		print 'next file'
		return
	df.fillna(0, inplace=True)
	df.convert_objects(convert_numeric=True)

	## set to either setUnique() or setMax()
	if unique is True:
		grouped = setUnique(df)
	else:
		grouped = setMax(df)


	## quantiles is qcut(), fixed width divisions is cut	
	grouped = quantize(quant_no,grouped)

	
	#turns into correct dictionary format for libpgm
	newDict = DFtoLibpgm(grouped)

# instantiate my learner 
	learner = PGMLearner()

# estimate structure
	try:
		result = learner.discrete_estimatebn(newDict)
	except:
		print 'error'
		#result = learner.discrete_estimatebn([dict([('a',1),('b',2)])])	
		return
# output
	return result


def bayesNetCont(textFile,unique):
	cleanText(textFile,'tempOutput.txt')

	## imports textFile into pandas
	try:
		df = pd.read_csv('tempOutput.txt', sep='\s+',dtype='float64',header=None)
	except:
		print 'next file'
		return
	df.fillna(0, inplace=True)
	df.convert_objects(convert_numeric=True)

	## set to either setUnique() or setMax()
	if unique is True:
		grouped = setUnique(df)
	else:
		grouped = setMax(df)

	
	#turns into correct dictionary format for libpgm
	newDict = DFtoLibpgm(grouped)

# instantiate my learner 
	learner = PGMLearner()

# estimate structure
	#gaussian
	try:
		result = learner.lg_constraint_estimatestruct(newDict)
	except:
		print 'error'
		return
		
# output
	return result

	

