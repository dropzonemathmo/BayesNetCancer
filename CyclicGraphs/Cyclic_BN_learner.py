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
from graphDrawer import *


##############################################################################
####################### REQUIRED FOR PATHWAYS DATA ###########################
##############################################################################

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



## INPUT: Directory path
## OUTPUT: Outputs all files in directory path
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)




##############################################################################
####################### DATA HANDLING TECHNIQUES #############################
##############################################################################

def quantize(number, dataFrame):
	for i, row in dataFrame.iterrows():
		## Required to try and except for rows of zeros to be ignored
		try:	
			dataFrame.ix[i] = pd.qcut(row,number,labels=False)
		except:
			print "next"
	return dataFrame



# makes repetitions of genes unique by appending row number
def setUnique(df):
	for i, row in df.iterrows():
     		df.ix[i,0] = df.ix[i,0]  +'_' + str(i)	
	return df.set_index([0], verify_integrity=True)

# sets repetitions to there maximum value
def setMax(df):
	return df.groupby([0]).max()

def setAverage(df):
	return df.groupby([0]).mean()

########################################################################
################# Functions for BAYES NET ALGORITHM ####################
########################################################################

# Function to calculate the joint probability table of two variables in the data set
def JPT(theData, varRow, varCol, noStates):
    jPT = zeros((noStates[varRow], noStates[varCol]), float )
#Coursework 1 task 3 should be inserted here 
    totalPoints = 0
    for aPoint in theData:
      jPT[aPoint[varRow]][aPoint[varCol]] += 1
      totalPoints += 1 
    for row in jPT:
      for i in range(noStates[varCol]):
	row[i] = row[i] / totalPoints
    return jPT


def MutualInformation(jP):
    mi=0.0
# mutual information formula

    margA = dot(jP,ones(jP.shape[1]))
    margB = dot(ones(jP.shape[0]),jP)
    
    for i, row in enumerate(jP):
      for j, element in enumerate(row):
	if element > 0:
	  mi += element*math.log((element/(margA[i]*margB[j])),2)
    
    return mi


def depScore(textFile,quant_no,unique):
#	

	grouped	= prepData(textFile,quant_no,unique)

	theData = grouped.transpose().as_matrix()		

	varNum = theData.shape[1]
	
	stateNum = zeros(varNum,int)
	for i in range(varNum):
		stateNum[i] = quant_no
	
	theDepMat = DependencyMatrix(theData, varNum,stateNum)
	theDepList = DependencyList(theDepMat)

	return sum(theDepList[:,0])/len(theDepList[:,0])


def prepData(df,quant_no,unique):
	
	## set to either setUnique() or setMax()
	if unique is True:
		grouped = setUnique(df)
	else:
		grouped = setAverage(df)
	
	## quantiles is qcut(), fixed width divisions is cut	
	grouped = quantize(quant_no,grouped)
	
	return grouped



def spanTree(textFile,quant_no,unique):

	grouped	= prepData(textFile,quant_no,unique)

	theData = grouped.transpose().as_matrix()		
	varNum = theData.shape[1]

	stateNum = zeros(varNum,int)
	for i in range(varNum):
		stateNum[i] = quant_no
	
	
	theDepMat = DependencyMatrix(theData, varNum,stateNum)
	
	theDepList = DependencyList(theDepMat)
	
	theSpanningTree = SpanningTreeAlgorithm(theDepList, varNum)

	nameIndex = list(grouped.transpose().columns.values)
	
	newSpanningTree = []

	for row in theSpanningTree:
		entry = [[row[0] , nameIndex[int(row[1])] , nameIndex[int(row[2])]]]
		newSpanningTree += entry
	
	
	return array(newSpanningTree)



#
# construct a dependency matrix for all the variables
def DependencyMatrix(theData, noVariables, noStates):
    MIMatrix = zeros((noVariables,noVariables))
# Coursework 2 task 2 should be inserted here
    for i in range(noVariables):
      for j in range(noVariables):
	 jP = JPT(theData,i,j,noStates)
	 MIMatrix[i][j] = MutualInformation(jP)

# end of coursework 2 task 2	
    return MIMatrix
# Function to compute an ordered list of dependencies 


def DependencyList(depMatrix):
    depList=[]
# Coursework 2 task 3 should be inserted here
    for i,row in enumerate(depMatrix):
      for j,element in enumerate(row):
	 if j < i:
	   depList += [[depMatrix[i][j],i,j]]

# end of coursework 2 task 3
    return array(depList)
#
# Functions implementing the spanning tree algorithm
# Coursework 2 task 4


parent = dict()
rank = dict()

def make_set(vertice):
	parent[vertice] = vertice
	rank[vertice] = 0

def find(vertice):
	if parent[vertice] != vertice:
		parent[vertice] = find(parent[vertice])
	return parent[vertice]

def union(vertice1, vertice2):
	root1 = find(vertice1)
	root2 = find(vertice2)
	if root1 != root2:
		if rank[root1] > rank[root2]:
			parent[root2] = root1
		else:
			parent[root1] = root2
			if rank[root1] == rank[root2]: rank[root2] += 1


def SpanningTreeAlgorithm(depList, noVariables):

    graphVertices = numpy.arange(0,noVariables,1)

    visitedNodes = []
	
    
    cyclicSpan = []
    sortedDepList = sorted(depList, key=operator.itemgetter(0), reverse=True)
    for w, v1, v2 in sortedDepList:
	if v1 not in visitedNodes: add v1
	if v2 not in visitedNodes: add v2
	
	cyclicSpan += [[w, v1, v2]]
	if visited_nodes.len = noVariables:
		break
 
    return cyclicSpan		
		


def writeTree(textFilePath,quant_no,unique,outputFile):
	try:
		df = pd.read_csv(textFilePath,header=None)
	except:
		print 'next file'
		return
	
	df.fillna(0, inplace=True)
	df.convert_objects(convert_numeric=True)

	## Takes as Input Panda DataFrame with column (0) as gene name and 0 for null values
	output = spanTree(df,quant_no,unique)
	score = depScore(df,quant_no,unique)
	print output
	print score
	if output is not None:
		output2 = pd.DataFrame(output)
		output2.to_csv(outputFile)
			


textFilePath = 'ZenaProbesProgressive'
quant_no = 3
unique = False # False - is max() , True - individuals
outputFile = textFilePath+str(quant_no)+'-'+str(unique)+'.csv'

writeTree(textFilePath+'.csv',quant_no,unique,outputFile)

outputGraph = textFilePath+str(quant_no)+'-'+str(unique)+'.png'

drawGraph(outputFile, outputGraph)


