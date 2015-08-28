from bayesLibraryDiscrete import *
import datetime
import time

from pandas import *

#ts = time.time()

#st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')




summary = DataFrame(columns=['gene_count','total'])

for textFile in findFiles('paths', '*.txt'):
	#print textFile
	cleanText(textFile,'tempOutput.txt')

	try:
		df = pd.read_csv('tempOutput.txt', sep='\s+',dtype='float64',header=None)
	except:
		summary.ix[textFile] = [0,0]
	grouped = df.groupby([0]).size()
	total = grouped.sum()
	geneCount = grouped.count()
	summary.ix[textFile]=[geneCount,total]


sortedTab = summary.sort(['total','gene_count'],ascending = True)

print sortedTab

sortedTab.to_csv('outputs/geneCount.csv',sep=',')


