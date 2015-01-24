"""
Edward M. Liu (eml2170)
CSOR W4246
HW6 Programming
Extra Credit
Dec 9, 2014
"""

#!/usr/bin/env python
import sys
import networkx as nx
from pulp import *
import matplotlib.pyplot as plt

def main():
	maxclique()

def maxclique():
	input_graph = sys.argv[1]
	G=nx.read_gml(input_graph)

	#Simply find maximum independent set of complement graph
	G=nx.complement(G)
	model = pulp.LpProblem('Maximum Independent Set', pulp.LpMaximize)
	V = G.nodes()
	E = G.edges()
	x = pulp.LpVariable.dict('x_%s', V, lowBound = 0, upBound = 1, cat = pulp.LpInteger)

	model += sum( x[i] for i in x)
	for (i,j) in E:
		model += sum( x[i]+x[j] ) <= 1
	
	model.solve()
	
	count = 0
	for i in x:
		if x[i].value() == 1:
			count += 1
	print count
	
if __name__ == "__main__":
    main()

