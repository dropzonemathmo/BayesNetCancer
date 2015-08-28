## INPUT: This file will read the CPDB_pathways_genes.txt file
## OUTPUT: Files named by pathway containing gene names

from numpy import genfromtxt
import json
import pandas as pd
import csv
import string
import os, fnmatch

# Finds all probes relating to a particular set of genes

TCGAgenes = pd.read_csv('TCGAGenes.csv')

for index, row in TCGAgenes.iterrows():
	print row['Genes']


with open("OutputProbes.json") as geneProbeJSON:
    geneToProbes = json.load(geneProbeJSON)

probes = pd.DataFrame(columns=('Probes', 'Genes'))

for index, row in TCGAgenes.iterrows():
	df= pd.DataFrame(geneToProbes[row['Genes']])
	df['Genes'] = row['Genes']
	df = df.rename(columns = {0:'Probes'})
	probes = probes.append(df, ignore_index = True)
print probes




#methylData = pd.read_csv('genomicMatrix.txt', sep='\s+', header=None)
#methylData.fillna(0, inplace=True)

#methylData = methylData.rename(columns = {0:'Probes'})
#probes = pd.merge(probes, methylData, on = 'Probes', how='left')

#probes.to_csv('ZenaProbes2.csv')



## INPUT: Directory path
## OUTPUT: Outputs all files in directory path
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)

print "finding files"
print findFiles('Data3', '*.txt')

n = 0

pd.show_versions(as_json=False)

for textFile in findFiles('Data3', '*'):
	print textFile
	methylData = pd.read_csv(textFile, sep='\s+', header=None)
	methylData.fillna(0, inplace=True)
	methylData = methylData.rename(columns = {0:'Probes'})
	result = pd.merge(probes, methylData, on = 'Probes', how = 'inner')
	#print result
	if n is 0:
		result2 = result
	result2 = result2.append(result, ignore_index = True)
	#print result2
	n = n + 1

result2.to_csv('ZenaProbes2.csv')
