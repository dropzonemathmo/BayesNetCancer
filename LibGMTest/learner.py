import json

from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork
from libpgm.pgmlearner import PGMLearner

# generate some data to use
nd = NodeData()
nd.load("grades.txt")    # an input file
skel = GraphSkeleton()
skel.load("grades.txt")
skel.toporder()
bn = DiscreteBayesianNetwork(skel, nd)
data = bn.randomsample(80000)

# instantiate my learner 
learner = PGMLearner()

# estimate structure
result = learner.discrete_constraint_estimatestruct(data)

# output
print json.dumps(result.E, indent=2)
