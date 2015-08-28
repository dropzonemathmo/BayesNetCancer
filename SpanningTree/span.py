import json
import pandas as pd
import csv
import numpy
import re
import os, fnmatch
import operator

from numpy import *
from math import *

# makes repetitions of genes unique by appending row number
def setUnique(df):
	for i, row in df.iterrows():
     		df.ix[i,0] = df.ix[i,0]  +'_' + str(i)	
	return df.set_index([0], verify_integrity=True)

# sets repetitions to there maximum value
def setMax(df):
	return df.groupby([0]).max()



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
# end of coursework 1 task 3
    return jPT

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


def quantize(number, dataFrame):
	for i, row in dataFrame.iterrows():
		dataFrame.ix[i] = pd.qcut(row,number).labels
	return dataFrame


def depScore(textFile,quant_no,unique):
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

	#print grouped

	theData = grouped.transpose().as_matrix()
	
	#print theData

	
	varNum = theData.shape[1]
	
	#print "varNum is "
	#print varNum

	stateNum = zeros(varNum,int)
	for i in range(varNum):
		stateNum[i] = quant_no
	
	#print "stateNum is "
	#print stateNum

	theDepMat = DependencyMatrix(theData, varNum,stateNum)
	
	#print "the Dep Mat is"
	#print theDepMat

	theDepList = DependencyList(theDepMat)


	return sum(theDepList[:,0])/len(theDepList[:,0])




def spanTree(textFile,quant_no,unique):
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
	#print grouped

	theData = grouped.transpose().as_matrix()	
#	print theData	

	varNum = theData.shape[1]
	
#	print "varNum is "
#	print varNum

	stateNum = zeros(varNum,int)
	for i in range(varNum):
		stateNum[i] = quant_no
	
	#print "stateNum is "
	#print stateNum

	theDepMat = DependencyMatrix(theData, varNum,stateNum)
#	
	print "the Dep Mat is"
	print theDepMat

	theDepList = DependencyList(theDepMat)



	theSpanningTree = SpanningTreeAlgorithm(theDepList, varNum)
	
	#print "the Spanning Tree is"	
	#print theSpanningTree

	nameIndex = list(grouped.transpose().columns.values)
	
	#print nameIndex	
	
	newSpanningTree = []

	for row in theSpanningTree:
		entry = [[row[0] , nameIndex[int(row[1])] , nameIndex[int(row[2])]]]
		newSpanningTree += entry
	
	
	return array(newSpanningTree)


def MutualInformation(jP):
    mi=0.0
# mutual information formula

    margA = dot(jP,ones(jP.shape[1]))
    margB = dot(ones(jP.shape[0]),jP)
    
    #print sum(jP)		
    #print "jP is ..."
    #print jP
    #print "marg probs A is"
    #print margA
    #print "marg probs B is"
    #print margB
		   
    for i, row in enumerate(jP):
      for j, element in enumerate(row):
	if element > 0:
	  mi += element*math.log((element/(margA[i]*margB[j])),2)
    

# end of coursework 2 task 1
    return mi
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

def SpanningTreeAlgorithm(depList, noVariables):
    spanningTree = []
    visitedNodes = []
    
    sortedDepList = sorted(depList, key=operator.itemgetter(0), reverse=True)
    count = 0
    
    for w , i , j in sortedDepList:
      #print visitedNodes
      if count == noVariables:
	break
      if i not in visitedNodes and j not in visitedNodes:
	visitedNodes += [i]
	visitedNodes += [j]
	spanningTree += [[w,i,j]]
	count += 1
      if i not in visitedNodes and j in visitedNodes:
	visitedNodes += [i]
	spanningTree += [[w,i,j]]
	count += 1
      if j not in visitedNodes and i in visitedNodes:
	visitedNodes += [j]
	spanningTree += [[w,i,j]]
	count += 1
    
    #print spanningTree
    return array(spanningTree)



#DEP()

#ADD_ARCS()

#theData = array(datain)



textFilePath = '../paths/"3-phosphoinositide biosynthesis".txt'
quant_no = 10
unique = False # False - is max() , True - individuals

def writeTree(textFilePath,quant_no,unique):
	with open('FirstTree.txt', 'w') as bayesTextFile:
		print textFilePath
		bayesTextFile.write(textFilePath+'\n')
		output = spanTree(textFilePath,quant_no,unique)
		score = depScore(textFilePath,quant_no,unique)
		print output
		print score
		if output is not None:
			bayesTextFile.write(output)
			score = depScore(textFilePath,quant_no,unique)

def writeAllTrees(mintot, maxtot, mingene, maxgene,unique, quant_no):

	# import table which details number of probes and genes in each file
	# there are multiple genes of the same name as, certain probes fix to different parts of the gene
	indexTab = pd.read_csv('../outputs/geneCount.csv')	
	indexTab.fillna(0, inplace=True)
	indexTab.convert_objects(convert_numeric=True)
	with open('outputs/bayesNetComb-disc-unique-'+str(unique)+'-mintot-'+str(mintot)+'-maxtot-'+str(maxtot)+'-mingene-'+str(mingene)+'-maxgene-'+str(maxgene)+'-quant_no-'+str(quant_no)+'.txt', 'w') as bayesTextFile:
		bayesTextFile.write('disc-unique-'+str(unique)+'-mintot-'+str(mintot)+'-maxtot-'+str(maxtot)+'-mingene-'+str(mingene)+'-maxgene-'+str(maxgene)+'-quant_no-'+str(quant_no)+'\n')			
		for i, row in indexTab.iterrows():
			if indexTab.ix[i,2] > mintot and indexTab.ix[i,2] < maxtot:
				if indexTab.ix[i,1] > mingene and indexTab.ix[i,1] < maxgene:
					textFilePath = '../'+indexTab.ix[i,0]
					print textFilePath
					bayesTextFile.write('\n'+textFilePath+'\n')
					output = spanTree(textFilePath,quant_no,unique)
					score = depScore(textFilePath,quant_no,unique)
					print output
					print score
					if output is not None:
						bayesTextFile.write(output)
						bayesTextFile.write(str(score))


# writeAllTrees(5,50,1,1000,True,10)
writeTree(textFilePath,quant_no,unique)


