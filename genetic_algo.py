import random
import graph2 as gp
import drone2 as dr

# Class for running multiple drones with genetic algorithm for multiple deliveries
def print_drone_paths(individual):
    for drone in individual:
        print(f'Drone {drone.name} Path: {[node.name for node in drone.locations]}')
        print(f'Drone {drone.name} Path: {[node.name for node in drone.path]}')


class Drones:
    # Initialize Drones object
    def __init__(self, name, graph: gp.Graph, initial_state: gp.Node, goals: [gp.Node], num_drones, mutation_rate):
        # Set attributes
        self.name = name
        self.state_space = graph
        self.initial_state = initial_state
        self.goal_states = goals
        self.num_drones = num_drones
        self.pop_size = 100
        self.population = []
        self.mutation_rate = mutation_rate

    # Method to create the initial population
    def create_population(self):
        for _ in range(self.pop_size):
            individual = [dr.Drone(n) for n in range(self.num_drones)]
            shuffled_goals = random.sample(self.goal_states, len(self.goal_states))
            for i, drone in enumerate(individual):
                start = i * len(shuffled_goals) // self.num_drones
                end = (i + 1) * len(shuffled_goals) // self.num_drones
                drone.locations.extend(shuffled_goals[start:end])
            self.population.append(individual)

    # Method to calculate the fitness of an individual
    def fitness_function(self, individual):
        total_cost = 0
        for drone in individual:
            cumulative_time = 0
            cumulative_utility_cost = 0

            for i, goal in enumerate(drone.locations):
                if i == 0:
                    distance = self.state_space.get_distance(self.initial_state, goal)
                else:
                    distance = self.state_space.get_distance(drone.locations[i - 1], goal)

                cumulative_time += distance
                utility_cost = cumulative_time * goal.delivery_urgency / 10
                cumulative_utility_cost += utility_cost

            total_cost += cumulative_time + cumulative_utility_cost

        return total_cost

    # Method to select individuals for breeding
    def select_individuals(self):
        parents = sorted(self.population, key=self.fitness_function)
        return parents[:self.pop_size // 2]

    # Method to perform uniform crossover
    def uniform_crossover(self, parent1, parent2):
        child1 = [dr.Drone(i) for i in range(self.num_drones)]
        child2 = [dr.Drone(i) for i in range(self.num_drones)]

        child1_assigned_goals = set()
        child2_assigned_goals = set()

        for drone in range(self.num_drones):
            for goal in parent1[drone].locations:
                if random.random() < 0.5 and goal not in child1_assigned_goals:
                    child1[drone].locations.append(goal)
                    child1_assigned_goals.add(goal)
                elif goal not in child2_assigned_goals:
                    child2[drone].locations.append(goal)
                    child2_assigned_goals.add(goal)

            for goal in parent2[drone].locations:
                if random.random() < 0.5 and goal not in child2_assigned_goals:
                    child2[drone].locations.append(goal)
                    child2_assigned_goals.add(goal)
                elif goal not in child1_assigned_goals:
                    child1[drone].locations.append(goal)
                    child1_assigned_goals.add(goal)

        self.add_missing_goals(child1, child1_assigned_goals)
        self.add_missing_goals(child2, child2_assigned_goals)

        return self.mutate(child1), self.mutate(child2)

    # Method to mutate individuals by balancing the number of goals assigned to each drone
    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            for _ in range(2):
                drone = random.randint(0, len(individual) - 1)
                while len(individual[drone].locations) == 0:
                    drone = random.randint(0, len(individual) - 1)

                goal = random.randint(0, len(individual[drone].locations) - 1)
                location = individual[drone].locations.pop(goal)
                empty_drones = [d for d in individual if len(d.locations) == 0]

                if empty_drones:
                    drone = random.choice(empty_drones)
                    drone.locations.append(location)
                else:
                    individual[random.randint(0, len(individual) - 1)].locations.append(location)
        return individual

    # Method to add missing goals to children if any
    def add_missing_goals(self, individual, assigned_goals):
        for goal in random.sample(self.goal_states, len(self.goal_states)):
            if goal not in assigned_goals:
                drone = random.randint(0, self.num_drones - 1)
                individual[drone].locations.append(goal)
                assigned_goals.add(goal)

    # Method to breed individuals
    def breed(self, parents):
        children = []
        for i in range(len(parents) - 1):
            child1, child2 = self.uniform_crossover(parents[i], parents[i + 1])
            children.append(child1)
            children.append(child2)

        child1, child2 = self.uniform_crossover(parents[0], parents[-1])
        children.append(child1)
        children.append(child2)

        return children

    # Method to run the genetic algorithm
    def genetic_alg(self):
        self.create_population()
        best_overall_solution = (self.population[0], float('inf'))

        for i in range(100):
            parents = self.select_individuals()
            best_solution = self.fitness_function(parents[0])
            if best_solution < best_overall_solution[1]:
                best_overall_solution = (parents[0], best_solution)
            print(f'Best Solution for Generation {i}: {best_solution}')
            self.population = self.breed(parents)

        print(f'Best Overall Solution: {best_overall_solution[1]}')
        return best_overall_solution
