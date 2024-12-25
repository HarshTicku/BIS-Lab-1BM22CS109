import random
import numpy as np
import matplotlib.pyplot as plt

class VehicleRoutingProblemACO:
    def __init__(self, customers, depot, n_vehicles, vehicle_capacity, demands, n_ants, n_iterations, alpha, beta, rho, q0):
        self.customers = customers
        self.depot = depot
        self.n_customers = len(customers)
        self.n_vehicles = n_vehicles
        self.vehicle_capacity = vehicle_capacity
        self.demands = demands
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha  # pheromone importance
        self.beta = beta    # heuristic information importance
        self.rho = rho      # pheromone evaporation rate
        self.q0 = q0        # probability for exploration vs exploitation
        self.pheromone = np.ones((self.n_customers + 1, self.n_customers + 1))  # pheromone initialization (depot + customers)
        self.distances = self.compute_distances()

    def compute_distances(self):
        points = np.vstack([self.depot, self.customers])
        distances = np.zeros((len(points), len(points)))
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                distance = np.linalg.norm(points[i] - points[j])
                distances[i][j] = distances[j][i] = distance
        return distances

    def select_next_customer(self, current, visited, remaining_demand):
        probabilities = np.zeros(self.n_customers + 1)
        tau = self.pheromone[current]
        eta = 1.0 / (self.distances[current] + 1e-10)

        for i in range(1, self.n_customers + 1):  # Skip depot (index 0)
            if i not in visited and self.demands[i - 1] <= remaining_demand:
                probabilities[i] = (tau[i] ** self.alpha) * (eta[i] ** self.beta)

        probabilities_sum = probabilities.sum()
        if probabilities_sum == 0:
            return 0  # Return to depot if no valid customers
        probabilities /= probabilities_sum  # Normalize probabilities

        if random.random() < self.q0:
            return np.argmax(probabilities)  # Exploitation
        else:
            return np.random.choice(range(len(probabilities)), p=probabilities)  # Exploration

    def construct_solution(self):
        solutions = []
        for _ in range(self.n_vehicles):
            visited = [0]  # Start at the depot
            tour = visited[:]
            remaining_demand = self.vehicle_capacity
            while True:
                current = visited[-1]
                next_customer = self.select_next_customer(current, visited, remaining_demand)
                if next_customer == 0:  # Return to depot
                    tour.append(0)
                    break
                visited.append(next_customer)
                tour.append(next_customer)
                remaining_demand -= self.demands[next_customer - 1]
            solutions.append(tour)
        return solutions

    def update_pheromones(self, ants_solutions, ants_lengths):
        self.pheromone *= (1 - self.rho)  # Evaporation
        for i in range(len(ants_solutions)):
            solution = ants_solutions[i]
            length = ants_lengths[i]
            for route in solution:
                for j in range(len(route) - 1):
                    from_city = route[j]
                    to_city = route[j + 1]
                    self.pheromone[from_city][to_city] += 1.0 / length
                    self.pheromone[to_city][from_city] += 1.0 / length

    def calculate_total_length(self, solution):
        total_length = 0
        for route in solution:
            for i in range(len(route) - 1):
                from_city = route[i]
                to_city = route[i + 1]
                total_length += self.distances[from_city][to_city]
        return total_length

    def optimize(self):
        best_solution = None
        best_length = float('inf')
        all_lengths = []

        for iteration in range(self.n_iterations):
            ants_solutions = []
            ants_lengths = []

            for _ in range(self.n_ants):
                solution = self.construct_solution()
                length = self.calculate_total_length(solution)
                ants_solutions.append(solution)
                ants_lengths.append(length)

                if length < best_length:
                    best_solution = solution
                    best_length = length

            self.update_pheromones(ants_solutions, ants_lengths)
            all_lengths.append(best_length)
            print(f"Iteration {iteration + 1}, Best Length: {best_length}")

        return best_solution, best_length, all_lengths

    def plot_solution(self, solution):
        plt.figure(figsize=(10, 6))
        for route in solution:
            x = [self.depot[0]] + [self.customers[city - 1][0] for city in route if city != 0] + [self.depot[0]]
            y = [self.depot[1]] + [self.customers[city - 1][1] for city in route if city != 0] + [self.depot[1]]
            plt.plot(x, y, marker='o')
        plt.title(f"Best Solution Length: {self.calculate_total_length(solution):.2f}")
        plt.show()


# Example VRP problem
depot = np.array([0, 0])
customers = np.array([
    [2, 4], [5, 2], [6, 6], [8, 3], [1, 3]
])
demands = [1, 2, 2, 1, 1]
vehicle_capacity = 4
n_vehicles = 2

# ACO parameters
n_ants = 10
n_iterations = 100
alpha = 1.0
beta = 2.0
rho = 0.5
q0 = 0.9

# Initialize and run the ACO for VRP
vrp_aco = VehicleRoutingProblemACO(customers, depot, n_vehicles, vehicle_capacity, demands, n_ants, n_iterations, alpha, beta, rho, q0)
best_solution, best_length, all_lengths = vrp_aco.optimize()

# Output and plot
print(f"Best Solution: {best_solution}")
print(f"Best Length: {best_length}")
vrp_aco.plot_solution(best_solution)
