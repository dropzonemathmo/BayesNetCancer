## INPUT: This file will read the CPDB_pathways_genes.txt file
## OUTPUT: Files named by pathway containing gene names


import string

fi = open('CPDB_pathways_genes.txt','r')

n = 0
for line in fi.read().split('"'):
    if n % 6 == 1:
	outLine = line.translate(string.maketrans("",""), string.punctuation) #removes punctuation from pathway name
	fo = open(outLine+'.txt','w')
    if n % 6 == 5:
	for gene in line.split(','):
	   fo.write(gene)
	   fo.write(';\n')
	fo.close()
    n = n + 1		
fi.close()

