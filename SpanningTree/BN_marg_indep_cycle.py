import json
import pandas as pd
import csv
import numpy
import re
import os, fnmatch
import operator
import networkx as nx
import matplotlib.pyplot as plt


from numpy import *
from math import *

from random import randint


from Cyclic_BN_learner import *

 

# Function to calculate the joint probability table of two variables in the data set
def JPT3(theData, varRow, varCol, varCent, noStates):
    jPT = zeros((noStates[varRow], noStates[varCol], noStates[varCent]), float )

    totalPoints = zeros(noStates[varCent])
    for aPoint in theData:
      jPT[aPoint[varCent]][aPoint[varRow]][aPoint[varCol]] += 1
      totalPoints[aPoint[varCent]] += 1 
    for k,row in enumerate(jPT): 	
      for i in range(noStates[varCol]):
	row[i] = row[i] / totalPoints[k]
    return jPT

def writeMargIndep(textFilePath,quant_no,unique,outputFile):
	try:
		df = pd.read_csv(textFilePath,header=None)
	except:
		print 'next file'
		return
	
	df.fillna(0, inplace=True)
	df.convert_objects(convert_numeric=True)

	grouped	= prepData(df,quant_no,unique)
	theData = grouped.transpose().as_matrix()		
	varNum = theData.shape[1]

	stateNum = zeros(varNum,int)
	for i in range(varNum):
		stateNum[i] = quant_no

	theDepMat = DependencyMatrix(theData, varNum,stateNum)
	
	theDepList = DependencyList(theDepMat)

	theSpanningTree = SpanningTreeAlgorithm(theDepList, varNum)


	colliderList = []
	for varA in range(0,varNum):
		for varCent in range(0,varNum):
			for varB in range(0,varNum):
				for row in theSpanningTree:
					#print "var A is"
					#print varA
					#print row[1]
					if (((varA-row[1]) == 0 and (varCent-row[2]) == 0) or ((varA-row[2]) == 0 and (varCent-row[1]) == 0)) and (varA - varB) != 0:
						for row2 in theSpanningTree:
							if ((varCent-row2[1]) == 0 and (varB-row2[2])==0) or ((varCent-row2[2]) == 0 and (varB-row2[1])==0) :
								jP3 = JPT3(theData,varA,varB,varCent,stateNum)
								condTot = 0
								for mat in jP3:
									cond = MutualInformation(mat)
									condTot += cond
	
#					
								jP = JPT(theData,varA,varB,stateNum)
		
	
								dep = MutualInformation(jP)		
#
								
								if condTot > COND_TOT_MIN and dep < DEP_MAX:
									colliderList += [[varA, varB, varCent,condTot,dep]]

	nameIndex = list(grouped.transpose().columns.values)
	
	newColliderList = []

	for row in colliderList:
		entry = [[nameIndex[int(row[0])] , nameIndex[int(row[1])] , nameIndex[int(row[2])],row[3],row[4]]]
		newColliderList += entry
	
	
	collidersDF = pd.DataFrame(newColliderList)
	collidersDF.to_csv(outputFile)
	print collidersDF

	return

COND_TOT_MIN = 0.20
DEP_MAX = 0.20			

textFilePath = 'ZenaProbesEntireData.csv'
quant_no = 3
unique = False
outputFile = 'ZenaProbesEntireDataCycleColliders.csv'

writeMargIndep(textFilePath,quant_no,unique,outputFile)

