import json

from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.lgbayesiannetwork import LGBayesianNetwork
from libpgm.pgmlearner import PGMLearner

# generate some data to use
nd = NodeData()
nd.load("gaussGrades.txt")    # an input file
skel = GraphSkeleton()
skel.load("gaussGrades.txt")
skel.toporder()
lgbn = LGBayesianNetwork(skel, nd)
data = lgbn.randomsample(8000)

print data

# instantiate my learner 
learner = PGMLearner()

# estimate structure
result = learner.lg_constraint_estimatestruct(data)

# output
print json.dumps(result.E, indent=2)
