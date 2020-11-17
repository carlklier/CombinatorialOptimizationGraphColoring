#%%
import dwavebinarycsp
from dwave.system import DWaveSampler, EmbeddingComposite
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from dimod import ExactSolver

provinces = ['a', 'b', 'c', 'd']
neighbors = [('a', 'b'), ('a', 'c'), ('b', 'c'), ('c', 'd')]

# Function for the constraint that two nodes with a shared edge not both select one color
# this code comes from https://docs.ocean.dwavesys.com/en/latest/examples/map_coloring.html
def not_both_1(v, u):
    return not (v and u)

# Function that plots a returned sample
def plot_map(sample, colors):
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
  for c in colors[0]:
    if c == 'R':
      colors_for_graph.append('Red')
    elif c == 'G':
      colors_for_graph.append('Green')
    elif c == 'B':
      colors_for_graph.append('dodgerblue')
    elif c=='Y':
      colors_for_graph.append('gold')
    else:
      colors_for_graph.append('Gray')
  return colors_for_graph  

def getColorMap(num_colors):
  if num_colors == 3:
    return {'001': 'R', '010': 'G', '100': 'B'}
  elif num_colors == 4:
    return {'0001': 'R', '0010': 'G', '0100': 'B', '1000': 'Y'}
  else:
    print("Color map for ", num_colors, " not implemented.")
    sys.exit(1)
  
def convert_sample_to_colors(samples, num_colors):
  colorMap = getColorMap(num_colors)
  colorCoded = []
  for k in samples:
    normal_array = list(k)
    colors = ''
    colorDigits = ''
    i = 0
    while i < len(k):
      for digit in normal_array[i:i+num_colors]:
        colorDigits += str(digit)
      try:
        colors += colorMap[colorDigits]
      except KeyError:
        colors += 'X'
      colorDigits = ''
      i += num_colors
    colorCoded.append(colors)
  return colorCoded

def create_variable_dict(variables, sample):
  new_sample = {}
  i = 0
  for variable in variables:
    new_sample[variable] = sample[i]
    i = i + 1
  return new_sample  

# Valid configurations for the constraint that each node select a single color
num_colors = 3
one_color_configurations = generate_color_configurations(num_colors)
print("One way color configurations: ", one_color_configurations)

# Create a binary constraint satisfaction problem
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

# Add constraint that each node (province) select a single color
# this code comes from https://docs.ocean.dwavesys.com/en/latest/examples/map_coloring.html
for province in provinces:
    variables = [province+str(i) for i in range(num_colors)]
    csp.add_constraint(one_color_configurations, variables)

# Add constraint that each pair of nodes with a shared edge not both select one color
# this code comes from https://docs.ocean.dwavesys.com/en/latest/examples/map_coloring.html
for neighbor in neighbors:
    v, u = neighbor
    for i in range(num_colors):
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

num_rec_to_see = 30
# Plotting all the engery values returned from sampling to get a sense of the variance
plt.figure(figsize=(40, 40))
bargraph = plt.bar(np.arange(len(records)), records['energy'], align='center')
plt.xlabel('Colorings', fontsize=30)
plt.ylabel('Energy Value', fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.show()

# Plotting the 15 lowest energy values labeled with the sample output
print("Printing records: ")
print(records[:num_rec_to_see])
plt.figure(figsize=(40, 40))
bargraph = plt.bar(np.arange(len(records[:num_rec_to_see])), records[:num_rec_to_see]['energy'], align='center')
plt.xticks(np.arange(len(records[:num_rec_to_see])), records[:num_rec_to_see]['sample'])
plt.xlabel('Colorings', fontsize=30)
plt.ylabel('Energy Value', fontsize=30)
plt.xticks(fontsize=30, rotation=70)
plt.yticks(fontsize=30)
ax = plt.gca()
ax.yaxis.offsetText.set_fontsize(30)
plt.show()

# Ploting the 15 lowest energy values labeled with RGB Colors
colorCodedTicks = convert_sample_to_colors(records[:num_rec_to_see]['sample'], num_colors)
plt.figure(figsize=(40, 40))
bargraph = plt.bar(np.arange(len(records[:num_rec_to_see])), records[:num_rec_to_see]['energy'], align='center')
plt.xticks(np.arange(len(records[:num_rec_to_see])), colorCodedTicks)
plt.xlabel('Colorings', fontsize=30)
plt.ylabel('Energy Value', fontsize=30)
plt.xticks(fontsize=30, rotation=70)
plt.yticks(fontsize=30)
ax = plt.gca()
ax.yaxis.offsetText.set_fontsize(30)
plt.show()

for record in records[:num_rec_to_see]:
  sample = record['sample']
  energy = record['energy']
  new_sample = create_variable_dict(sampleset.variables, sample)
  colored_sample = convert_sample_to_colors([sample], num_colors)
  colors = getColors(colored_sample)
  if not csp.check(new_sample):
      #plot_map(new_sample, colors)
      print("Sample: ", new_sample)
      print("Energy Value: ", energy)
      print("Failed to color graph validly")
      plot_map(new_sample, colors)
  else:
      print("Sample: ", new_sample)
      print("Energy Value: ", energy)
      plot_map(new_sample, colors)
#%%