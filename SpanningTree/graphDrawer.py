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




## INPUT: Directory path
## OUTPUT: Outputs all files in directory path
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)




def drawGraph(inputFile, outputFile):
	listEdge = pd.read_csv(inputFile)
	arrayList = listEdge.ix[:,[2,3]].as_matrix()
	arrayList
	G = nx.from_edgelist(arrayList)
	limits=plt.axis('off')
	
	nx.draw_networkx(G,with_labels=True, font_size=5, node_size=500)
	plt.savefig(outputFile)



