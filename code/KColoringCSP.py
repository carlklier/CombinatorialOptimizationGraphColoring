#%%
# This code comes from https://docs.ocean.dwavesys.com/en/latest/examples/map_coloring.html
import dwavebinarycsp
from dwave.system import DWaveSampler, EmbeddingComposite
import networkx as nx
import matplotlib.pyplot as plt

# Represent the map as the nodes and edges of a graph
#provinces = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
#neighbors = [('AB', 'BC'), ('AB', 'NT'), ('AB', 'SK'), ('BC', 'NT'), ('BC', 'YT'), ('MB', 'NU'),
#             ('MB', 'ON'), ('MB', 'SK'), ('NB', 'NS'), ('NB', 'QC'), ('NL', 'QC'), ('NT', 'NU'),
#             ('NT', 'SK'), ('NT', 'YT'), ('ON', 'QC')]
# provinces = ['1', '2', '3', '4', '5']
# neighbors = [('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('2', '3'), ('2', '4'),
#              ('2', '5'), ('3', '4'), ('3', '5'), ('4', '5')]

# Creating the same graph as Nachiket
provinces = ['a', 'b', 'c', 'd']
neighbors = [('a', 'b'), ('b', 'c'), ('a', 'c'), ('c', 'd')]

# Function for the constraint that two nodes with a shared edge not both select one color
def not_both_1(v, u):
    return not (v and u)

# Function that plots a returned sample
def plot_map(sample):
    G = nx.Graph()
    G.add_nodes_from(provinces)
    G.add_edges_from(neighbors)
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

# Set up a solver using the local system’s default D-Wave Cloud Client configuration file
# and sample 1000 times
sampler = EmbeddingComposite(DWaveSampler())
sampleset = sampler.sample(bqm, num_reads=100)
records = sampleset.record
records.sort(order='energy')

print("printing info: ", sampleset.info)
print("printing timing info: ", sampleset.info['timing'])
print("printing labels: ", sampleset.variables)
print("length of records: ", len(records))
print("first 15 samples: ", records[:15])
print("Printing keys: ", records[0].dtype)
# Plot the lowest-energy sample if it meets the constraints
sample = sampleset.first.sample
if not csp.check(sample):
    print("Sample: ", sample)
    plot_map(sample)
    print("Failed to color map")
else:
    print("Sample: ", sample)
    plot_map(sample)

#%%    