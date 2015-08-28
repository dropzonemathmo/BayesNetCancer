## INPUT: This file will read the CPDB_pathways_genes.txt file
## OUTPUT: Files named by pathway containing gene names

from numpy import genfromtxt
import json
import pandas as pd
import csv
import string

fi = open('CPDB_pathways_genes.txt','r')


with open("OutputProbes.json") as geneProbeJSON:
    geneToProbes = json.load(geneProbeJSON)

n = 0
for line in fi.read().split('"'):
    if n % 6 == 1:
	outLine = line.translate(string.maketrans("",""), string.punctuation) #removes punctuation from pathway name
	fo = open(outLine+'.txt','w')
    if n % 6 == 5:
	for gene in line.split(','):
	   fo.write(gene)
	   fo.write('-')	
	   if gene in geneToProbes.keys():	
	   	fo.write(':'.join(geneToProbes[gene]))
	   fo.write(';\n')
	fo.close()
    n = n + 1		
fi.close()

