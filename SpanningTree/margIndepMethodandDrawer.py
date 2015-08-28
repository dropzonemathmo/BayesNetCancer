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


textFilePath = 'ZenaProbes3.csv'
quant_no = 3
unique = False # False - is max() , True - individuals

def writeTree(textFilePath,quant_no,unique):
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
		output2.to_csv('nim1.txt')
	return output

def writeMargIndep(textFilePath,quant_no,unique):
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

	print "the spanning tree is"
	print theSpanningTree

	#for row in theSpanningTree:
	#	print "row is "
	#	print row
	#	print row[1]
	#	print row[2]
	colliderList = []
	for varA in range(0,varNum):
		#print varA
		for varCent in range(0,varNum):
			#print varCent
			for varB in range(0,varNum):
		#		print varB
				for row in theSpanningTree:
					#print "var A is"
					#print varA
					#print row[1]
					if (((varA-row[1]) == 0 and (varCent-row[2]) == 0) or ((varA-row[2]) == 0 and (varCent-row[1]) == 0)) and (varA - varB) != 0:
						for row2 in theSpanningTree:
							if ((varCent-row2[1]) == 0 and (varB-row2[2])==0) or ((varCent-row2[2]) == 0 and (varB-row2[1])==0) :
#								print "triple has been found"
#								print varA
#								print varCent
#								print varB

								jP3 = JPT3(theData,varA,varB,varCent,stateNum)
								condTot = 0
								for mat in jP3:
									cond = MutualInformation(mat)
									condTot += cond
	
#					
								jP = JPT(theData,varA,varB,stateNum)
		
	
								dep = MutualInformation(jP)		
#
								
							#	print "varA is"
							#	print varA
							#	print "varCent is"
							#	print varCent
							#	print "varB is"
							#	print varB
							#	print "condTot is"
							#	print condTot

							#	print "dep is"
							#	print dep

								if condTot > 0.20 and dep < 0.20:
									colliderList += [[varA, varB, varCent,condTot,dep]]

	nameIndex = list(grouped.transpose().columns.values)
	
	newColliderList = []

	for row in colliderList:
		entry = [[nameIndex[int(row[0])] , nameIndex[int(row[1])] , nameIndex[int(row[2])],row[3],row[4]]]
		newColliderList += entry
	
	#print theSpanningTree

	return array(newColliderList)	
#	return colliderList
			
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



############################################################################
############### BOOTSTRAPPER ###############################################

def sampler(textFilePath,quant_no,unique):
	try:
		df = pd.read_csv(textFilePath,header=None)
	except:
		print 'next file'
		return
	
	df.fillna(0, inplace=True)
	df.convert_objects(convert_numeric=True)
	
	n = df.shape[1] - 1

	boost = df[[0]]
	
	for j in range(1,100):	

		for i in range(1,n):
	## pick a random number between 0 and n

			k = randint(0,n)
			column = df[[k]]
			boost[i] = column
		## append column x to dataframe

		## build df as before
	
		print boost
		## Takes as Input Panda DataFrame with column (0) as gene name and 0 for null values
		output = spanTree(boost,quant_no,unique)
		score = depScore(boost,quant_no,unique)
		print output
		print score
	 
		if output is not None:
			output2 = pd.DataFrame(output)
			output2.to_csv('boost/sample'+str(j)+'.csv')



# writeAllTrees(5,50,1,1000,True,10)
#writeTree(textFilePath,quant_no,unique)

#sampler(textFilePath,quant_no,unique)


listEdge = writeTree(textFilePath, quant_no,unique)

listEdge = listEdge[:, [1, 2]]

print listEdge

G = nx.from_edgelist(listEdge)
limits=plt.axis('off')

#read_edgelist(listEdge, nodetype=int, data=(('weight',float),))


nx.draw_networkx(G,with_labels=True, font_size=5, node_size=500)
plt.savefig("niMpath.png")


colliders = writeMargIndep(textFilePath,quant_no,unique)
print colliders

