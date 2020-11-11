#%%
# This code comes from https://docs.ocean.dwavesys.com/en/latest/examples/map_coloring.html
import dwavebinarycsp
from dwave.system import DWaveSampler, EmbeddingComposite
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from dimod import ExactSolver

# Represent the map as the nodes and edges of a graph
# provinces = ['1', '2', '3', '4']
# neighbors = [('1', '2'), ('1', '3'), ('1', '4'), ('2', '3'), ('2', '4'), ('3', '4')]

provinces = ['a', 'b', 'c']
neighbors = [('a', 'b'), ('a', 'c'), ('b', 'c')]

# Function for the constraint that two nodes with a shared edge not both select one color
def not_both_1(v, u):
    return not (v and u)

# Function that plots a returned sample
def plot_map(sample, colors):
    print("Colors inside plot: ", colors)
    G = nx.Graph()
    G.add_nodes_from(provinces)
    G.add_edges_from(neighbors)
    nx.draw_circular(G, with_labels=True, node_color=colors, node_size=1000, cmap=plt.cm.rainbow)
    plt.show()

def generate_color_configurations(n):
  color_configurations = []
  for i in range(n):
    color = [0] * n
    color[i] = 1
    color_configurations.append(tuple(color))
  return color_configurations

def getColors(colors):
  colors_for_graph = []
  for c in reversed(colors[0]):
    if c == 'R':
      colors_for_graph.append('Red')
    elif c == 'G':
      colors_for_graph.append('Green')
    elif c == 'B':
      colors_for_graph.append('dodgerblue')
    else:
      colors_for_graph.append('Gray')
  return colors_for_graph  

def convert_sample_to_colors(samples):
  colorMap = {'001': 'R', '010': 'G', '100': 'B'}
  colorCoded = []
  for k in samples:
    normal_array = list(k)
    colors = ''
    colorDigits = ''
    i = 0
    while i < len(k):
      for digit in normal_array[i:i+3]:
        colorDigits += str(digit)
      try:
        colors += colorMap[colorDigits]
      except KeyError:
        colors += 'X'
      colorDigits = ''
      i += 3
    colorCoded.append(colors)
  return colorCoded

def create_variable_dict(variables, sample):
  print("sample inside create_variable_dict: ", sample)
  new_sample = {}
  i = 0
  for variable in variables:
    print("This is sample[i]: ", sample[i])
    new_sample[variable] = sample[i]
    i = i + 1
  print("new sample inside create_variable_dict:  ", new_sample)
  return new_sample  

# Valid configurations for the constraint that each node select a single color
colors = 3
one_color_configurations = generate_color_configurations(colors)
print("One way color configurations: ", one_color_configurations)

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

sampler = ExactSolver()
sampleset = sampler.sample(bqm)
records = sampleset.record
records.sort(order='energy')

print("printing info: ", sampleset.info)
print("printing labels: ", sampleset.variables)
print("length of records: ", len(records))

plt.figure(figsize=(40, 40))
bargraph = plt.bar(np.arange(len(records)), records['energy'], align='center')
plt.xlabel('Colorings', fontsize=30)
plt.ylabel('Energy Value', fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.show()


print("Printing keys: ", records[0].dtype)
print("Printing records: ", records[:15])
plt.figure(figsize=(40, 40))
bargraph = plt.bar(np.arange(len(records[:15])), records[:15]['energy'], align='center')
plt.xticks(np.arange(len(records[:15])), records[:15]['sample'])
plt.xlabel('Colorings', fontsize=30)
plt.ylabel('Energy Value', fontsize=30)
plt.xticks(fontsize=30, rotation=70)
plt.yticks(fontsize=30)
plt.show()

colorCodedTicks = convert_sample_to_colors(records[:15]['sample'])
plt.figure(figsize=(40, 40))
bargraph = plt.bar(np.arange(len(records[:15])), records[:15]['energy'], align='center')
plt.xticks(np.arange(len(records[:15])), colorCodedTicks)
plt.xlabel('Colorings', fontsize=30)
plt.ylabel('Energy Value', fontsize=30)
plt.xticks(fontsize=30, rotation=70)
plt.yticks(fontsize=30)
plt.show()


# Plot the lowest-energy sample if it meets the constraints
for sample in records['sample'][:5]:
  new_sample = create_variable_dict(sampleset.variables, sample)
  colored_sample = convert_sample_to_colors([sample])
  print("This is colored sample: ", colored_sample)
  colors = getColors(colored_sample)
  print("This is returned colores: ", colors)
  if not csp.check(new_sample):
      print("Sample: ", new_sample)
      plot_map(new_sample, colors)
      print("Failed to color map")
  else:
      print("Sample: ", new_sample)
      plot_map(new_sample, colors)


#%%