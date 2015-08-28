from numpy import genfromtxt
import json

#SOME GENES ARE MISSING THEREFORE HAVE TO USE FOLLOWING FORM

# firstCol = genfromtxt('FullDatasetProbeToGeneMappings.txt',invalid_raise=False, usemask=False,filling_values=0.0, usecols=(0,1,2))
# print firstCol
# secondCol = genfromtxt('FullDatasetProbeToGeneMappings.txt',invalid_raise=False,usemask=False,filling_values=0.0,usecols=(3),skip_footer=1)


# secondCol=append(secondCol, 0.0)
# secondCol=secondCol.reshape(3,1)
# firstCol=hstack([firstCol,secondCol])

# print firstCol

import pandas as pd
import csv

	
df = pd.read_csv('FullDatasetProbeToGeneMappings2.txt', sep='\s+', header=None)
df.fillna(0, inplace=True)

#result = df.groupby([3]).groups

del df[1]
del df[2]

print df

g = df.groupby([3])
result = g[0].apply(lambda s : s.tolist())
result2 = result.to_dict()

#groupedProbes = result
 	
#print result.get_group("SELS")
#result.to_json('OutputProbes.json')

with open('OutputProbes.json','w') as fp:
	json.dump(result2,fp)


#print(my_data[1][1])

 #   datain = []
  #  for line in range(noDataPoints):
   #     datain.append(map(int,((f.readline()).split())))
   # f.close()

#fi = open('FullDatasetProbeToGeneMappings.txt','r')


#d = {}

#for index, row in df.iterrows():
#	gene = row[3]
#	site = row[0]
	# print gene, site
#	if gene in d.keys():
#		d[gene] = d[gene]+str(site)+';'
 #  	else:
 #       	d[gene] = str(site)+';'


#w = csv.writer(open("GenesPathwayString.csv", "w"))
#for key, val in d.items():
 #   w.writerow([key, val])
		


