import networkx as nx
import matplotlib.pyplot as plt
import math

def create_grouped_graph(m, n):
    G = nx.Graph()
    G.add_node(0, label=1)

    if n % 4 == 0 or n % 4 == 2 or n % 4 == 3:
        for i in range(1, math.ceil(n/4) + 2):
            group_center = i * m + 1
            G.add_node(group_center)
            if i == 1:
                G.nodes[group_center]['label'] = 1
            else:
                G.nodes[group_center]['label'] = 3 * i - 2
            G.add_edge(0, group_center)

            for j in range(2, m + 1):
                node = i * m + j
                G.add_node(node)
                G.nodes[node]['label'] = j
                G.add_edge(group_center, node)

        for i in range(math.ceil(n/4) + 1, n + 1):
            group_center = i * m + 1
            G.add_node(group_center)
            G.nodes[group_center]['label'] = 2 * math.ceil(n/4) + i
            G.add_edge(0, group_center)

            for j in range(2, m+1):
                node = i * m + j
                j=j-1
                G.add_node(node)
                G.nodes[node]['label'] = n+i+j-1-2*math.ceil(n/4)
                G.add_edge(group_center, node)
    if n % 4 == 1:
        for i in range(1, math.ceil(n/4)+1):
            group_center = i * m + 1
            G.add_node(group_center)
            if i == 1:
                G.nodes[group_center]['label'] = 1
            else:
                G.nodes[group_center]['label'] = 3 * i - 2
            G.add_edge(0, group_center)
            if i< math.ceil(n/4):
              for j in range(2, m + 1):
                  node = i * m + j
                  G.add_node(node)
                  G.nodes[node]['label'] = j
                  G.add_edge(group_center, node)
            if i== math.ceil(n/4):
              for j in range(2, m + 1):
                  node = i * m + j
                  G.add_node(node)
                  if j == 3:
                    G.nodes[node]['label'] = n-math.ceil(n/4)+3
                  else:
                    G.nodes[node]['label'] = j
                  G.add_edge(group_center, node)

        for i in range(math.ceil(n/4)+1, n+1):
            group_center = i * m + 1
            G.add_node(group_center)
            G.nodes[group_center]['label'] = 2 * math.ceil(n/4) + i - 1
            G.add_edge(0, group_center)
            for j in range(2, m + 1):
                  node = i * m + j
                  G.add_node(node)
                  G.nodes[node]['label'] = n+i+j-1-2*math.ceil(n/4)
                  G.add_edge(group_center, node)

    return G

def draw_grouped_graph(G):
    pos = nx.spring_layout(G, k=0.4, seed=41)
    labels = {node: G.nodes[node].get('label', '') for node in G.nodes() if G.nodes[node].get('label') is not None}
    nx.draw(G, pos, labels=labels, node_size=500, node_color='skyblue')
    plt.show()

def store_edge_weights_and_check_uniqueness(G, m, n):
    edge_weights = set()
    max_label = 0

    for edge in G.edges():
        source_label = G.nodes[edge[0]].get('label', None)
        target_label = G.nodes[edge[1]].get('label', None)

        if source_label is not None and target_label is not None:
            edge_weight = source_label + target_label
            edge_weights.add(edge_weight)
            max_label = max(max_label, source_label, target_label)

    max_allowed_label = math.ceil((m * n + 1) / 2)
    are_all_edges_unique = len(edge_weights) == len(set(G.edges()))

    return edge_weights, are_all_edges_unique, max_label, max_label <= max_allowed_label

# Example usage
m = 3
n = 8
graph = create_grouped_graph(m, n)
draw_grouped_graph(graph)

# Check edge weights and label validity
edge_weights, are_all_edges_unique, max_label, is_max_label_valid = store_edge_weights_and_check_uniqueness(graph, m, n)


# Additional prints
labels = {node: graph.nodes[node].get('label', '') for node in graph.nodes() if graph.nodes[node].get('label') is not None}
print("Labels of vertices:", labels)
print("Weights of edges:", edge_weights)
print("Are all edges unique?", are_all_edges_unique)
print("Max Label:", max_label)
print("Is max label valid?", is_max_label_valid)