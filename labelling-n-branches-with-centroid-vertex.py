import networkx as nx
import matplotlib.pyplot as plt
import math

def create_grouped_graph(m, n):
    G = nx.Graph()
    # Add center vertex and label it as 1
    G.add_node(0, label=1)
    # Check if n % 4 equals 0, 2, or 3
    if n % 4 == 0 or n % 4 == 2 or n % 4 == 3:
        group_centers = []
        for i in range(1, math.ceil(n/4) + 2):
            group_center = i * m + 1
            G.add_node(group_center)
            group_centers.append(group_center)
            if i == 1:
                G.nodes[group_center]['label'] = 1
            else:
                G.nodes[group_center]['label'] = 3 * i - 2
            G.add_edge(0, group_center)
            if i > 1:
                prev_group_center = (i - 1) * m + 1
                G.add_edge(prev_group_center, group_center)
            for j in range(2, m + 1):
                node = i * m + j
                G.add_node(node)
                G.nodes[node]['label'] = j
                G.add_edge(group_center, node)
        for i in range(math.ceil(n/4) + 1, n + 1):
            group_center = i * m + 1
            G.add_node(group_center)
            group_centers.append(group_center)
            G.nodes[group_center]['label'] = 2 * math.ceil(n/4) + i
            G.add_edge(0, group_center)
            prev_group_center = (i - 1) * m + 1
            G.add_edge(prev_group_center, group_center)
            for j in range(2, m+1):
                node = i * m + j
                j=j-1
                G.add_node(node)
                G.nodes[node]['label'] = n+i+j-1-2*math.ceil(n/4)
                G.add_edge(group_center, node)
        G.add_edge(group_centers[-1], group_centers[0])
    return G
def draw_grouped_graph(G):
    pos = nx.spring_layout(G, k=0.1,seed=342)
    labels = {node: G.nodes[node].get('label', '') for node in G.nodes() if G.nodes[node].get('label') is not None}
    nx.draw(G, pos, labels=labels, node_size=500, node_color='skyblue')
    plt.show()

def store_edge_weights_and_check_max_label(G, m, n):
    edge_weights = {}
    vertex_labels = {}

    for node in G.nodes():
        label = G.nodes[node].get('label')
        if label is not None:
            vertex_labels[node] = label

    max_label = 0
    for edge in G.edges():
        source_label = vertex_labels.get(edge[0], None)
        target_label = vertex_labels.get(edge[1], None)

        if source_label is not None and target_label is not None:
            edge_weight = source_label + target_label  # Calculate edge weight
            edge_weights[edge] = edge_weight

            max_label = max(max_label, source_label, target_label)

    max_allowed_label = math.ceil((m * n + 1) / 2)
    return edge_weights, vertex_labels, max_label, max_label <= max_allowed_label

def calculate_order(m, n):
    return n*m + 1

def calculate_size(m, n):
    return n*(m-1 + 2)


# Example usage
m = 3  # Number of vertices per group
n = 8  # Number of groups

# Create the grouped graph
graph = create_grouped_graph(m, n)
draw_grouped_graph(graph)

# Calculate and print order and size of the graph
order = calculate_order(m, n)
size = calculate_size(m, n)
print(f"Order of the graph: {order}")
print(f"Size of the graph: {size}")

# Check edge weights and label validity
edge_weights, vertex_labels, max_label, is_max_label_valid = store_edge_weights_and_check_max_label(graph, m, n)
print("Edge Weights:", edge_weights)
print("Vertex Labels:", vertex_labels)
print("Max Label:", max_label)
print("Is max label valid?", is_max_label_valid)
