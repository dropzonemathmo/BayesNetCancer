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


## Input File

path = "testGraph.csv"


try:
	df = pd.read_csv(textFilePath,header=None)
except:
	print 'next file'
	return



# Function to calculate the joint probability table of two variables in the data set
def JPT3(theData, varRow, varCol, varCent, noStates):
    jPT = zeros((noStates[varRow], noStates[varCol], noStates[varCent]), float )
#Coursework 1 task 3 should be inserted here 
    totalPoints = 0
    for aPoint in theData:
      jPT[aPoint[varRow]][aPoint[varCol]][aPoint[varCent]] += 1
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


#def margIndep(var1,var2,varcent):
#	create JPT(var1,var2,varcent)
	


#def condIndep(var1,var2):

	

## make list of variables

## Find Triples

## arrange variable names in list

# for i = 1:n-2{
#	for j = i+1:n-1{
#		for  k = j+1:n{
#
#		edge A = i-j
#		edge B = j-k
#		check edge A and edge B are in list of edges{
			## Work out marginal 
			## Work out conditional dependence

#			if (marginal big and conditional small){
#				add variable that is in both edge A and edge B to collider list
#				direct edge A
#				direct edge B

#			}
#		}
#	}			
#}

## propagate all other edges


## 

