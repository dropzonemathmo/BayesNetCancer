from bayesLibrary import *
import datetime
import time

ts = time.time()
textFilePath = 'paths/"thyronamine and iodothyronamine metabolism".txt'
quant_no = 2
unique = False # False - is max()

st = datetime.datetime.fromtimestamp(ts).strftime('%y-%m-%d %H:%M:%S')

def writeDiscrete(textFilePath,quant_no,unique):
	with open('outputs/bayesNetsSingle'+'- discrete - ' + str(quant_no) + '- unique - ' + str(unique)+'.txt', 'w') as bayesTextFile:
		print textFilePath
		bayesTextFile.write(textFilePath+'\n')
		bayesTextFile.write('discrete - ' + str(quant_no) + '- unique - ' +str(unique)+'\n')
		output = bayesNetDiscrete(textFilePath,quant_no,unique)
		if output is not None:
			text = json.dumps(output.E,indent =2)
			bayesTextFile.write(text)


def writeCont(textFilePath, unique):
	with open('outputs/bayesNetsSingle - cont - unique - ' + str(unique)+'.txt', 'w') as bayesTextFile:
		print textFilePath
		bayesTextFile.write(textFilePath+'\n')
		bayesTextFile.write('cont - unique - ' +str(unique)+'\n')
		output = bayesNetCont(textFilePath,unique)
		if output is not None:
			text = json.dumps(output.E,indent =2)
			bayesTextFile.write(text)



writeCont(textFilePath,unique)
