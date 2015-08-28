import json

from libpgm.graphskeleton import GraphSkeleton
from libpgm.nodedata import NodeData
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork
from libpgm.tablecpdfactorization import TableCPDFactorization

# load nodedata and graphskeleton
nd = NodeData()
skel = GraphSkeleton()
nd.load("grades.txt")
skel.load("grades.txt")

# toporder graph skeleton
skel.toporder()

# load evidence
evidence = dict(Letter='weak')

# load bayesian network
bn = DiscreteBayesianNetwork(skel, nd)

# load factorization
fn = TableCPDFactorization(bn)

# sample 
result = fn.gibbssample(evidence, 1000)

# output
print json.dumps(result, indent=2)
