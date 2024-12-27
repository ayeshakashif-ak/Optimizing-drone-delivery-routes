import random
import math
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import io
import base64

# Graph class

class Graph:
    def __init__(self, width=400, height=400, num_nodes=10):
        self.width = width
        self.height = height
        self.num_nodes = num_nodes
        self.nodes = {}
        self.create_nodes()
        self.connect_nodes()

    def create_nodes(self):
        # Create a central hub node
        hub_pos = (self.width // 2, self.height // 2)
        self.nodes['Hub'] = Node('Hub', hub_pos)

        min_distance = (self.width + self.height) / 20
        max_attempts = 1000

        for i in range(1, self.num_nodes):
            pos = None
            for _ in range(max_attempts):
                pos = (random.randint(0, self.width), random.randint(0, self.height))
                if all(euc_dist(node.pos, pos) >= min_distance for node in self.nodes.values()):
                    break
            self.nodes[f'N-{i}'] = Node(f'N-{i}', pos)

    # Create connections of nodes in graph
    def connect_nodes(self):
        weather_conditions = ["Sunny", "Cloudy", "Rainy", "Foggy"]

        weather_speeds = {
            "Sunny": 35,
            "Cloudy": 30,
            "Rainy": 25,
            "Foggy": 15
        }

        # Ensure every node is connected to at least one other node
        for node in self.nodes.values():
            for other_node in self.nodes.values():
                if node != other_node and other_node not in node.neighbors:
                    distance = euc_dist(node.pos, other_node.pos)
                    weather = random.choice(weather_conditions)
                    speed = weather_speeds[weather]
                    travel_cost = int((distance / speed) * 60)
                    node.neighbors[other_node] = [distance, weather, travel_cost]
                    other_node.neighbors[node] = [distance, weather, travel_cost]

    def get_distance(self, node1, node2):
        # Retrieve distance from neighbors if directly connected
        if node2 in node1.neighbors:
            return node1.neighbors[node2][0]  # The first element in neighbors' data is the distance
        else:
            raise ValueError(f"No direct connection between {node1.name} and {node2.name}")
    def plot_graph(self, goals, drones=None, animate=False):
        # Create figure
        f, ax = plt.subplots(figsize=(11, 10))

        # Define color mappings for weather
        weather_colors = {
            "Sunny": "yellow",
            "Cloudy": "orange",
            "Rainy": "lightblue",
            "Foggy": "limegreen"
        }

        # Helper function to plot connections
        def plot_connection(node1, node2, color, width):
            ax.plot([node1.pos[0], node2.pos[0]], [node1.pos[1], node2.pos[1]], color=color, linewidth=3)

        # Plot all node connections
        for node in self.nodes.values():
            for neighbor, data in node.neighbors.items():
                plot_connection(node, neighbor, weather_colors[data[1]], 1)
                mid_x, mid_y = (node.pos[0] + neighbor.pos[0]) / 2, (node.pos[1] + neighbor.pos[1]) / 2
                ax.text(mid_x, mid_y, f"{data[0]:.1f}mi, {data[2]}min", fontsize=8, color="black")

        # Plot nodes
        for node in self.nodes.values():
            color = 'blue' if node.name == 'Hub' else 'purple'
            size = 25 if node.name == 'Hub' else 15
            ax.plot(node.pos[0], node.pos[1], 'o', markersize=size, color=color)
            ax.text(node.pos[0], node.pos[1], node.name, ha='center', va='center', fontsize=9, color='white')

        # Add weather legend
        weather_patches = [mpatches.Patch(color=color, label=f"{condition}") for condition, color in
                           weather_colors.items()]
        weather_legend = ax.legend(handles=weather_patches, title="Weather Conditions", loc='upper right')
        ax.add_artist(weather_legend)  # Ensure the weather legend is added before other legends

        # Plot drone paths
        if drones:
            drone_colors = cm.get_cmap('rainbow', len(drones))
            drone_patches = []

            for i, drone in enumerate(drones):
                color = drone_colors(i)
                drone_patches.append(mpatches.Patch(color=color, label=f'Drone {i + 1}'))
                for j in range(len(drone.path) - 1):
                    start, end = drone.path[j], drone.path[j + 1]
                    ax.annotate("", xy=end.pos, xytext=start.pos,
                                arrowprops=dict(arrowstyle="->", color=color, linewidth=2))

            # Add drone legend
            drone_legend = ax.legend(handles=drone_patches, title="Drones", loc='upper left')
            ax.add_artist(drone_legend)  # Ensure the drone legend doesn't overwrite the weather legend

        # Add animation for drones
        if animate and drones:
            drone_positions = [[drone.path[0].pos] for drone in drones]
            drone_dots = [ax.plot([], [], 'ro', markersize=8)[0] for _ in drones]

            def update(frame):
                for i, drone in enumerate(drones):
                    if frame < len(drone.path):
                        pos = drone.path[frame].pos
                        drone_dots[i].set_data(*pos)
                return drone_dots

            ani = animation.FuncAnimation(
                f, update, frames=max(len(drone.path) for drone in drones),
                blit=True, interval=500  # Adjust interval for speed
            )

            # Save the animation to a BytesIO stream
            buffer = io.BytesIO()
            ani.save(buffer, format='gif', writer=PillowWriter(fps=2))
            buffer.seek(0)

            # Embed the animation in Streamlit
            data = base64.b64encode(buffer.read()).decode('utf-8')
            return f'<img src="data:image/gif;base64,{data}" />'

        # Return static plot if no animation
        plt.show()
        return f


    # Function to return selected nodes
    def select_nodes(self, selected_names):
        # Initialize list of selected nodes
        selected_nodes = []
        # Loop through all nodes in graph
        for node in self.nodes.values():
            # Check if node name is in selected names
            if node.name in selected_names:
                # Add node to selected nodes list
                selected_nodes.append(node)
        # Return list of selected nodes
        return selected_nodes


# Euclidean distance function
def euc_dist(a, b):
    return math.sqrt(
        math.pow(a[0]-b[0], 2) +
        math.pow(a[1]-b[1], 2)
    )

# Function to print names of path
def retrieve_path_names(path):
    # Check if path is None
    if path is None:
        # Return no path found
        return 'No path found'
    # If path is not None
    else:
        # Initialize path string
        path_str = ''
        # Loop through all nodes in path
        for i in range(len(path)-1):
            # Add name of node to path string
            path_str += path[i].name + ' -> '
        # Add last node name to path string
        path_str += path[len(path)-1].name
        # Return path string
        return path_str

# Node class
class Node:
    # Initialize node with name and position
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        # Initialize delivery urgency of node
        self.delivery_urgency = 0
        # Initialize neighbors of node
        self.neighbors = {}
