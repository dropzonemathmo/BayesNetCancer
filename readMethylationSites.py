from numpy import genfromtxt
import json
import pandas as pd
import csv

	
df = pd.read_csv('FullDatasetProbeToGeneMappings2.txt', sep='\s+', header=None)
df.fillna(0, inplace=True)

del df[1]
del df[2]

print df

g = df.groupby([3])
result = g[0].apply(lambda s : s.tolist())
result2 = result.to_dict()

with open('OutputProbes.json','w') as fp:
	json.dump(result2,fp)


