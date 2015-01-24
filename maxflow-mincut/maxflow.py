"""
Edward M. Liu (eml2170)
CSOR W4246
HW4 Programming
Nov 14, 2014
"""

#!/usr/bin/env python
import sys
import networkx as nx


input_graph = sys.argv[1]
s = sys.argv[2]
t = sys.argv[3]
G=nx.read_gml(input_graph)
# print degree for each team - number of games
for u,v,a in G.edges(data=True):
	a['capacity']=1
print nx.maximum_flow_value(G,int(s),int(t))