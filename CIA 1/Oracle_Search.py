import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx
import sys
import heapq

graph = {}
heuristics = []
G = nx.Graph()  
MAX_NODES = 26  

def add_edge(from_node, to_node, cost):
    graph[from_node].append((to_node, cost))
    G.add_edge(get_node(from_node), get_node(to_node), weight=cost)

def get_index(c):
    return ord(c) - ord('A')

def get_node(index):
    return chr(index + ord('A'))


def oracle_search(start, goal):
    queue = []
    heapq.heappush(queue, (0, start)) 
    
    costs = {start: 0}
    came_from = {start: None}
    
    while queue:
        current_cost, current_node = heapq.heappop(queue)
        
        if current_node == goal:
            return reconstruct_path(came_from, start, goal)
        
        for next_node, edge_cost in graph[current_node]:
            new_cost = costs[current_node] + edge_cost
            if next_node not in costs or new_cost < costs[next_node]:
                costs[next_node] = new_cost
                priority = new_cost + heuristics[next_node] 
                heapq.heappush(queue, (priority, next_node))
                came_from[next_node] = current_node
    
    return None 

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse() 
    return path

# Visualization
def draw_graph(path_to_highlight=None):
    plt.clf()
    
    pos = nx.spring_layout(G)
    node_labels = {node: f"{node}({heuristics[get_index(node)]})" for node in G.nodes()}
    
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color='lightblue', font_weight='bold', node_size=500, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    if path_to_highlight:
        path_labels = [get_node(p) for p in path_to_highlight]
        edge_list = [(path_labels[i], path_labels[i + 1]) for i in range(len(path_labels) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='r', width=2)
    
    plt.show() 

def process_graph():
    global graph, heuristics, G
    graph.clear()
    G.clear()
    
    try:
        nodes = node_input.get().split() 
        if not nodes:
            raise ValueError("No nodes provided.")
        
        graph = {i: [] for i in range(len(nodes))}

        heuristics_input = heuristics_input_entry.get().split() 
        if not heuristics_input:
            raise ValueError("No heuristics provided.")
        
        heuristics = list(map(int, heuristics_input)) 
        if len(heuristics) != len(nodes):
            raise ValueError("Mismatch between number of nodes and heuristics.")

        edges = edge_input.get("1.0", tk.END).strip().split("\n")  
        if not edges:
            raise ValueError("No edges provided.")
        
        for edge in edges:
            parts = edge.split()
            if len(parts) != 3:
                raise ValueError(f"Invalid edge format: {edge}")
            
            from_node, to_node, cost = parts
            from_idx = get_index(from_node)
            to_idx = get_index(to_node)
            add_edge(from_idx, to_idx, int(cost))

        start_menu['menu'].delete(0, 'end')
        goal_menu['menu'].delete(0, 'end')
        
        for node in nodes:
            start_menu['menu'].add_command(label=node, command=tk._setit(start_var, node))
            goal_menu['menu'].add_command(label=node, command=tk._setit(goal_var, node))
        
        start_var.set(nodes[0])  
        goal_var.set(nodes[-1]) 

        draw_graph()

    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def run_search():
    start = get_index(start_var.get())
    goal = get_index(goal_var.get())
    
    path = oracle_search(start, goal)
    
    if path:
        result_label.config(text="Path: " + " -> ".join(get_node(p) for p in path))
        draw_graph(path) 
    else:
        result_label.config(text="No path found")

# GUI Setup
root = tk.Tk()
root.title("Visualization")
root.geometry("400x400")

tk.Label(root, text="Enter nodes (e.g. A B):").pack()
node_input = tk.Entry(root)
node_input.pack()

tk.Label(root, text="Enter heuristics (e.g. 4 0):").pack()
heuristics_input_entry = tk.Entry(root)
heuristics_input_entry.pack()

tk.Label(root, text="Enter edges (e.g. A B 1, one per line):").pack()
edge_input = tk.Text(root, height=5, width=30)
edge_input.pack()

tk.Label(root, text="Start node:").pack()
start_var = tk.StringVar()
start_menu = tk.OptionMenu(root, start_var, '')
start_menu.pack()

tk.Label(root, text="Goal node:").pack()
goal_var = tk.StringVar()
goal_menu = tk.OptionMenu(root, goal_var, '')
goal_menu.pack()

process_button = tk.Button(root, text="Get Graph", command=process_graph)
process_button.pack()

run_button = tk.Button(root, text="Search Path", command=run_search)
run_button.pack()

result_label = tk.Label(root, text="Result will be shown here")
result_label.pack()

root.mainloop()
