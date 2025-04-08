import re

grafo = {1: [(2, 13, 1, True), (4, 17, 1, True)], 2 :[(1, 13, 1, True)]}

print(grafo[1][0][0])

for n in grafo: 
    for a in grafo[n]: 
        if (a[0], )