"""
Edward M. Liu (eml2170)
CSOR W4246
HW4 Programming
Nov 14, 2014
Disclaimer: This code is based off an example with PuLP I found online at http://blog.sommer-forst.de/tag/minimum-cost-flow/
The lp and input is different however.
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

arcData = {}
for u,v,a in G.edges(data=True):
	a['capacity']=1
	key = u,v
	arcData[key]=[0,1]

# list of nodes
nodes = G.nodes()
nodes.remove(int(s))
nodes.remove(int(t))

arcs = G.edges()

# Splits the dictionaries to be more understandable
(mins, maxs) = splitDict(arcData) 

# Creates the boundless Variables as Integers
vars = LpVariable.dicts("Route",arcs,None,None,LpInteger)

flow_edges = G.out_edges(int(s))
target_edges = G.in_edges(int(t))

for a in arcs:
	vars[a].bounds(mins[a], maxs[a])
	

# Creates the 'prob' variable to contain the problem data    
prob = LpProblem("Max Flow Problem Sample",LpMaximize)

# Creates the objective function
prob += lpSum([vars[a] for a in flow_edges]), "Total flow in network"


# Creates all problem constraints - this ensures the amount going into each node is 
# at least equal to the amount leaving
for n in nodes:
    prob += (lpSum([vars[(i,j)] for (i,j) in arcs if j == n]) ==
             lpSum([vars[(i,j)] for (i,j) in arcs if i == n])), \
            "Flow Conservation in Node %s"%n
prob += (lpSum([vars[a] for a in target_edges]) == lpSum([vars[a] for a in flow_edges])), "Target conservation"

 
# The problem data is written to an .lp file

prob.writeLP("maxflow.lp")
 
# The problem is solved using PuLP's choice of Solver

prob.solve()
 
# The optimised objective function value is printed to the screen    
print int(value(prob.objective))