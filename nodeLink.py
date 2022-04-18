##----------------------------------------------------------------------------##
## Description
##
##
##
##

## Import 
import matplotlib.pyplot as plt
import networkx as nx

nxG = nx.Graph()

nxG.add_node(2)
nxG.add_edge(1,2)

nx.draw(nxG)
plt.savefig("filename.png")
