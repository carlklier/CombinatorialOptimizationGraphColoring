#%%
import dwavebinarycsp
from dwave.system import DWaveSampler, EmbeddingComposite
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Graph 1
provinces1 = ['a', 'b', 'c', 'd']
neighbors1 = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]

# Graph 2
provinces2 = ['a', 'b', 'c', 'd', 'e', 'f']
neighbors2 = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('b', 'e'), ('e', 'f'), ('d', 'f')]

# Graph 3
provinces3 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
neighbors3 = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('b', 'e'), ('e', 'f'), ('d', 'f'), ('e', 'g'), ('g', 'h'), ('f', 'h')]

#Graph 4
provinces4 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
neighbors4 = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('b', 'e'), ('e', 'f'), ('d', 'f'), ('e', 'g'), ('g', 'h'), ('f', 'h'), ('g', 'i'), ('i', 'j'), ('h', 'j')]

#Graph 5
provinces5 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
neighbors5 = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('b', 'e'), ('e', 'f'), ('d', 'f'), ('e', 'g'), ('g', 'h'), ('f', 'h'), ('g', 'i'), ('i', 'j'), ('h', 'j'), ('i', 'k'), ('k', 'l'), ('j', 'l')]

graph_list = [[provinces1, neighbors1], [provinces2, neighbors2], [provinces3, neighbors3], [provinces4, neighbors4], [provinces5, neighbors5]]

# Function for the constraint that two nodes with a shared edge not both select one color
# This code comes from https://docs.ocean.dwavesys.com/en/latest/examples/map_coloring.html
def not_both_1(v, u):
    return not (v and u)

def generate_color_configurations(n):
  color_configurations = []
  for i in range(n):
    color = [0] * n
    color[i] = 1
    color_configurations.append(tuple(color))
  return color_configurations

# Valid configurations for the constraint that each node select a single color
colors = 4
graphs = 5
one_color_configurations = generate_color_configurations(colors)
timings = []

for i in range(graphs):
  # Create a binary constraint satisfaction problem
  csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

  # Add constraint that each node (province) select a single color
  # This code comes from https://docs.ocean.dwavesys.com/en/latest/examples/map_coloring.html
  for province in graph_list[i][0]:
    variables = [province+str(i) for i in range(colors)]
    csp.add_constraint(one_color_configurations, variables)

  # Add constraint that each pair of nodes with a shared edge not both select one color
  # This code comes from https://docs.ocean.dwavesys.com/en/latest/examples/map_coloring.html
  for neighbor in graph_list[i][1]:
    v, u = neighbor
    for i in range(colors):
        variables = [v+str(i), u+str(i)]
        csp.add_constraint(not_both_1, variables)

  # Convert the binary constraint satisfaction problem to a binary quadratic model
  bqm = dwavebinarycsp.stitch(csp)

  sampler = EmbeddingComposite(DWaveSampler())
  sampleset = sampler.sample(bqm, num_reads=8000)
  records = sampleset.record
  records.sort(order='energy')

  timings.append(sampleset.info['timing']['qpu_access_time'])

print("timings: ", timings)
plt.plot(['graph1', 'graph2', 'graph3', 'graph4', 'graph5'], timings, 'ro--')
plt.ylabel('qpu_access_time')
plt.show()
#%%