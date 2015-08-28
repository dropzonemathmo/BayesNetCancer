#from numpy import genfromtxt
import json
import pandas as pd
import csv
import numpy
import re
import os, fnmatch

from bayesLibrary import *
from bayesSingle import *

from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.lgbayesiannetwork import LGBayesianNetwork
from libpgm.pgmlearner import PGMLearner




#print lines

mintot = 10
maxtot = 20
mingene = 5
maxgene = 100

quant_no = 2
unique = True



def bayesContPrint(mintot, maxtot, mingene, maxgene, unique):
	indexTab = pd.read_csv('outputs/geneCount.csv')	
	indexTab.fillna(0, inplace=True)
	indexTab.convert_objects(convert_numeric=True)

	with open('outputs/bayesNetComb-cont-unique-'+str(unique)+'-mintot-'+str(mintot)+'-maxtot-'+str(maxtot)+'-mingene-'+str(mingene)+'-maxgene-'+str(maxgene)+'.txt', 'w') as bayesTextFile:
		bayesTextFile.write('cont-unique-'+str(unique)+'-mintot-'+str(mintot)+'-maxtot-'+str(maxtot)+'-mingene-'+str(mingene)+'-maxgene-'+str(maxgene)+'\n')			
		for i, row in indexTab.iterrows():
			if indexTab.ix[i,2] > mintot and indexTab.ix[i,2] < maxtot:
				if indexTab.ix[i,1] > mingene and indexTab.ix[i,1] < maxgene:
					textFilePath = indexTab.ix[i,0]
					print textFilePath
					bayesTextFile.write('\n'+textFilePath+'\n')
					bayesTextFile.write('geneCount ' + str(indexTab.ix[i,1]) + ' total ' + str(indexTab.ix[i,2])+'\n')
					output = bayesNetCont(textFilePath,unique)
					if output is not None:
						text = json.dumps(output.E,indent =2)
						bayesTextFile.write(text)

def bayesDiscPrint(mintot, maxtot, mingene, maxgene,unique, quant_no):
	indexTab = pd.read_csv('outputs/geneCount.csv')	
	indexTab.fillna(0, inplace=True)
	indexTab.convert_objects(convert_numeric=True)
	with open('outputs/bayesNetComb-disc-unique-'+str(unique)+'-mintot-'+str(mintot)+'-maxtot-'+str(maxtot)+'-mingene-'+str(mingene)+'-maxgene-'+str(maxgene)+'-quant_no-'+str(quant_no)+'.txt', 'w') as bayesTextFile:
		bayesTextFile.write('disc-unique-'+str(unique)+'-mintot-'+str(mintot)+'-maxtot-'+str(maxtot)+'-mingene-'+str(mingene)+'-maxgene-'+str(maxgene)+'-quant_no-'+str(quant_no)+'\n')			
		for i, row in indexTab.iterrows():
			if indexTab.ix[i,2] > mintot and indexTab.ix[i,2] < maxtot:
				if indexTab.ix[i,1] > mingene and indexTab.ix[i,1] < maxgene:
					textFilePath = indexTab.ix[i,0]
					print textFilePath
					bayesTextFile.write('\n'+textFilePath+'\n')
					bayesTextFile.write('geneCount ' + str(indexTab.ix[i,1]) + ' total ' + str(indexTab.ix[i,2])+'\n')
					output = bayesNetDiscrete(textFilePath,quant_no,unique)
					if output is not None:
						text = json.dumps(output.E,indent =2)
						bayesTextFile.write(text)

## Max 5 - 20 genes

## Discrete
# bayesDiscPrint(1,1000,5,50,False,2)
# bayesDiscPrint(1,1000,5,50,False,3)
# bayesDiscPrint(1,1000,5,50,False,4)

## Cont
# bayesContPrint(1,1000,5,50,False)


## Unique

## Discrete
bayesDiscPrint(5,50,1,1000,True,2)
bayesDiscPrint(5,50,1,1000,True,3)
bayesDiscPrint(5,50,1,1000,True,4)

## Cont
bayesContPrint(5,50,1,1000,True)

