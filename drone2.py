import graph2 as gp


# Define Drone class
class Drone:
    # Initialize Drone object
    def __init__(self, name):
        self.name = name
        # List of goal assigned to the drone
        self.locations: [gp.Node] = []
        # Cost of the drone path
        self.cost = 0
        # Full path of the drone (includes paths between goals)
        self.path = []


