"""
Edward M. Liu (eml2170)
CSOR W4246
HW6 Programming
Dec 9, 2014
"""

#!/usr/bin/env python
import sys
import networkx as nx
from pulp import *

def main():
	method1()
	method2()
	method3()

def method1():
	input_graph = sys.argv[1]
	G=nx.read_gml(input_graph)
	max = 0
	for i in range(0,10):
		size = len(nx.maximal_independent_set(G))
		print size
		if size > max:
			max = size
	print max

def method2():
	input_graph = sys.argv[1]
	G=nx.read_gml(input_graph)

	#initialize maximization problem
	model = pulp.LpProblem('Maximum Independent Set', pulp.LpMaximize)
	V = G.nodes()
	E = G.edges()

	#Define variables, one for each vertex
	x = pulp.LpVariable.dict('x_%s', V, lowBound = 0, upBound = 1, cat = pulp.LpInteger)

	#Add constraints
	model += sum( x[i] for i in x)
	for (i,j) in E:
		model += sum( x[i]+x[j] ) <= 1
	
	#Solve
	model.solve()
	
	#Find value of objective function
	count = 0
	for i in x:
		if x[i].value() == 1:
			count += 1
	print count

	
def method3():
	input_graph = sys.argv[1]
	G=nx.read_gml(input_graph)

	model = pulp.LpProblem('Maximum Independent Set', pulp.LpMaximize)
	V = G.nodes()
	E = G.edges()
	
	#Allow variables to be continuous
	x = pulp.LpVariable.dict('x_%s', V, lowBound = 0, upBound = 1)

	model += sum( x[i] for i in x)
	for (i,j) in E:
		model += sum( x[i]+x[j] ) <= 1
	
	model.solve()
	
	count = 0
	for i in x:
		count += x[i].value()
	print count
if __name__ == "__main__":
    main()

