#%%
# This code comes from https://docs.ocean.dwavesys.com/en/latest/examples/map_coloring.html
import dwavebinarycsp
from dwave.system import DWaveSampler, EmbeddingComposite
import networkx as nx
import matplotlib.pyplot as plt
import sys

# Represent the map as the nodes and edges of a graph
provinces = ['1', '2', '3', '4', '5']
neighbors = [('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('2', '3'), ('2', '4'),
             ('2', '5'), ('3', '4'), ('3', '5'), ('4', '5')]

# Function for the constraint that two nodes with a shared edge not both select one color
def not_both_1(v, u):
    return not (v and u)

# Function that plots a returned sample
def plot_map(sample, G):
    # Translate from binary to integer color representation
    color_map = {}
    for province in provinces:
          for i in range(colors):
            if sample[province+str(i)]:
                color_map[province] = i
    # Plot the sample with color-coded nodes
    node_colors = [color_map.get(node) for node in G.nodes()]
    nx.draw_circular(G, with_labels=True, node_color=node_colors, node_size=1000, cmap=plt.cm.rainbow)
    plt.show()

def generate_color_configurations(n):
  color_configurations = []
  for i in range(n):
    color = [0] * n
    color[i] = 1
    color_configurations.append(tuple(color))
  return color_configurations

G = nx.Graph()
G.add_nodes_from(provinces)
G.add_edges_from(neighbors)
max_chromatic_num = max(G.degree)[1] + 1
chromatic_num = 0
if(len(provinces)==0):
  print("Chromatic number is %" %chromatic_num)
  sys.exit(0)
elif(len(provinces) == 1):
  chromatic_num = 1
  print("Chromatic number is %" %chromatic_num)
  sys.exit(0)
else:
  print("Graph has more than 1 node, chromatic number cannot be 0 or 1.")
  chromatic_num = 2
while(chromatic_num <= max_chromatic_num):
# Valid configurations for the constraint that each node select a single color
  colors = chromatic_num
  one_color_configurations = generate_color_configurations(colors)
  print(one_color_configurations)

  # Create a binary constraint satisfaction problem
  csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

  # Add constraint that each node (province) select a single color
  for province in provinces:
      variables = [province+str(i) for i in range(colors)]
      csp.add_constraint(one_color_configurations, variables)

  # Add constraint that each pair of nodes with a shared edge not both select one color
  for neighbor in neighbors:
      v, u = neighbor
      for i in range(colors):
          variables = [v+str(i), u+str(i)]
          csp.add_constraint(not_both_1, variables)

  # Convert the binary constraint satisfaction problem to a binary quadratic model
  bqm = dwavebinarycsp.stitch(csp)

  # Set up a solver using the local system’s default D-Wave Cloud Client configuration file
  # and sample 1000 times
  sampler = EmbeddingComposite(DWaveSampler())
  sampleset = sampler.sample(bqm, num_reads=4000)


  # Plot the lowest-energy sample if it meets the constraints
  sample = sampleset.first.sample
  if not csp.check(sample):
      print(sample)
      plot_map(sample)
      print("Failed to find a %s-coloring for this graph." % chromatic_num)
  else:
      print(sample)
      print("Found a %s-coloring for this graph." % chromatic_num)
      plot_map(sample)
  chromatic_num = chromatic_num + 1