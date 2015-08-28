from numpy import genfromtxt
import json
import pandas as pd
import csv

	
df = pd.read_csv('genomicMatrix2.txt', sep='\s+', header=None)
df.fillna(0, inplace=True)

df2 = df.set_index([0])

print df2

print df2.loc['cg13332474']

# print g

#result = g[2].apply(lambda s : s.tolist())
#result2 = result.to_dict()

#print result2

#with open('OutputGenes.json','w') as fp:
#	json.dump(result2,fp)


