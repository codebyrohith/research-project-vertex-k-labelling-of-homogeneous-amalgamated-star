import networkx as nx
import matplotlib.pyplot as plt
import math

# Function to create a grouped graph
def create_grouped_graph(m, n):
    G = nx.Graph()  # Initialize an empty graph
    labels_list = []  # List to store unique labels

    # Add center node with label 1
    G.add_node(0, label=1)
    labels_list.append(1)

    label_increment = 0  # Initialize label increment
    # Create group centers and their associated nodes
    for i in range(1, n + 1):
        group_center = i * m + 1
        G.add_node(group_center)

        # Assign labels to group centers
        if i == 1:
            G.nodes[group_center]['label'] = 1
        else:
            label_increment += math.ceil((m * n + 1) / 2) / (n - 1)
            G.nodes[group_center]['label'] = int(label_increment)
            labels_list.append(int(label_increment) + 1)

        # Connect group centers to the central node
        G.add_edge(0, group_center)

        # Add nodes and edges within each group
        for j in range(2, m + 1):
            node = i * m + j
            G.add_node(node)
            G.add_edge(group_center, node)

    # Assign labels to child nodes based on group center labels
    for i in range(1, n + 1):
        parent_label2 = G.nodes[m * i + 1]['label']
        for j in range(2, m + 1):
            child_node = i * m + j
            for k in range(3, math.ceil(m * n + 1 / 2) + 1):
                if parent_label2 + k not in labels_list:
                    child_label = k
                    value_to_store = k + parent_label2
                    labels_list.append(value_to_store)
                    G.nodes[child_node]['label'] = child_label
                    break

    return G, labels_list

# Function to draw the graph
def draw_grouped_graph(G):
    pos = nx.spring_layout(G, k=0.4, seed=51)  # Positioning nodes
    labels = {node: G.nodes[node].get('label', '') for node in G.nodes() if G.nodes[node].get('label') is not None}
    nx.draw(G, pos, labels=labels, node_size=500, node_color='skyblue')  # Draw graph
    plt.show()

# Function to store edge weights and check uniqueness
def store_edge_weights_and_check_uniqueness(G, m, n):
    edge_weights = set()  # Set to store unique edge weights
    non_unique_edge_weights = set()  # Set to store non-unique edge weights
    max_label = 0  # Initialize max label

    # Calculate edge weights and find max label
    for edge in G.edges():
        source_label = G.nodes[edge[0]].get('label', None)
        target_label = G.nodes[edge[1]].get('label', None)

        if source_label is not None and target_label is not None:
            edge_weight = source_label + target_label
            if edge_weight in edge_weights:
                non_unique_edge_weights.add(edge_weight)
            else:
                edge_weights.add(edge_weight)

            max_label = max(max_label, source_label, target_label)

    max_allowed_label = math.ceil((m * n + 1) / 2)
    are_all_edges_unique = len(edge_weights) == len(set(G.edges()))

    if not are_all_edges_unique:
        print("Non-unique edge weights:", non_unique_edge_weights)

    return edge_weights, are_all_edges_unique, max_label, max_label <= max_allowed_label

# Example usage
m = 4
n = 7
graph, labels_list = create_grouped_graph(m, n)

draw_grouped_graph(graph)

# Check edge weights and label validity
edge_weights, are_all_edges_unique, max_label, is_max_label_valid = store_edge_weights_and_check_uniqueness(graph, m, n)
labels = {node: graph.nodes[node].get('label', '') for node in graph.nodes() if graph.nodes[node].get('label') is not None}

print("Labels of vertices:", labels)
print("Weights of edges:", edge_weights)
print("Are all edges unique?", are_all_edges_unique)
print("Max Label:", max_label)
print("Is max label valid?", is_max_label_valid)