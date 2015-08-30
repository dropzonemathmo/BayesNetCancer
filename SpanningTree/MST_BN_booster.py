import json
import pandas as pd
import csv
import numpy
import re
import os, fnmatch
import operator

from numpy import *
from math import *

from random import randint

from MST_BN_learner import *



def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)



def boostCount(boostDir,outputFile):
	freqTable = pd.DataFrame(columns=('Gene1', 'Gene2','Count'))

	for textFile in findFiles(boostDir, '*'):
		
		boost = pd.read_csv(textFile, sep=',', header=None)
	
	
		for index, row in boost.iterrows():
			if freqTable[(freqTable.Gene1 == row[2])&(freqTable.Gene2 == row[3])].empty:
				df = pd.DataFrame([[row[2],row[3],1]], columns = ['Gene1','Gene2','Count'])
				freqTable = freqTable.append(df, ignore_index=True)
			else:	
				freqTable.Count[(freqTable.Gene1 == row[2])&(freqTable.Gene2 == row[3])] += 1
			freqTable.convert_objects(convert_numeric=True)

	freqTable.to_csv(outputFile+'.csv')



def sampler(textFilePath,quant_no,unique):
	try:
		df = pd.read_csv(textFilePath+'.csv',header=None)
	except:
		print 'next file'
		return
	
	df.fillna(0, inplace=True)
	df.convert_objects(convert_numeric=True)
	
	n = df.shape[1] - 1

	boost = df[[0]]
	os.mkdir('boost'+textFilePath)
	
	for j in range(1,100):	

		for i in range(1,n):
	## pick a random number between 0 and n
			k = randint(0,n)
			column = df.ix[:,[k]]
			boost[i] = column
	
		output = spanTree(boost,quant_no,unique)
		score = depScore(boost,quant_no,unique)
	 
		if output is not None:
			output2 = pd.DataFrame(output)
			output2.to_csv('boost'+textFilePath+'/sample'+str(j)+'.csv')

textFilePath = 'ZenaProbesProgressive'
quant_no = 3
unique = False

sampler(textFilePath,quant_no,unique)

boostCount('boost'+textFilePath,'boostCount'+textFilePath)

