"""
Edward M. Liu (eml2170)
CSOR W4246
HW4 Programming
Nov 14, 2014
"""

#!/usr/bin/env python

# Import PuLP modeller functions
from pulp import *
import sys
import networkx as nx

input_graph = sys.argv[1]
s = sys.argv[2]
t = sys.argv[3]
G=nx.read_gml(input_graph)
D=nx.read_gml(input_graph)
G = nx.DiGraph(D)

bounds = {}
gdata = []
for u,v,a in G.edges(data=True):
	a['capacity']=1
	key = u,v
	bounds[key]=[0,1]
	gdata.append((u,v))

for node in G.nodes():
	gdata.append(node)
	bounds[node]=[0,1]


# Splits the dictionaries to be more understandable
(mins, maxs) = splitDict(bounds) 

# Creates the boundless Variables as Integers
vars = LpVariable.dicts("Q_i,j",gdata,None,None,LpInteger)

for a in gdata:
	vars[a].bounds(mins[a], maxs[a])

# Creates the 'prob' variable to contain the problem data    
prob = LpProblem("Min Cut Problem Sample",LpMinimize)

# Creates the objective function
prob += lpSum([1*vars[a] for a in G.edges()]), "Min cut"

# Creates all problem constraints
for e in G.edges():
	i = e[0]
	j = e[1]
	prob += ((vars[j] - vars[i]) <= vars[(i,j)])

prob += ((vars[int(t)] - vars[int(s)]) == 1), "S_T constraint"
# The problem data is written to an .lp file

prob.writeLP("minflow.lp")
 
# The problem is solved using PuLP's choice of Solver

prob.solve()
 
# The optimised objective function value is printed to the screen    
print int(value(prob.objective))