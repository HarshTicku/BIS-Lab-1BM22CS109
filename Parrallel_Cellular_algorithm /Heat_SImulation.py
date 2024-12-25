print("Dhanush C")
print("1BM22CS085")
import numpy as np
import matplotlib.pyplot as plt

# Parameters
grid_size = (50, 50)  # Grid dimensions
dt = 0.5  # Time step
diffusion_coefficient = 0.1  # Diffusion constant
n_iter = 50  # Number of iterations

# Initialize the grid
temperature = np.zeros(grid_size)

# Set initial conditions
source_position = (25, 25)  # Heat source location
temperature[source_position] = 100  # Initial temperature at the source

# Define neighborhood interaction (Laplace operator for diffusion)
def update_temperature(temperature):
    new_temperature = temperature.copy()
    for x in range(1, grid_size[0] - 1):
        for y in range(1, grid_size[1] - 1):
            # Calculate diffusion based on the average of neighboring cells
            new_temperature[x, y] += diffusion_coefficient * dt * (
                temperature[x + 1, y] + temperature[x - 1, y] +
                temperature[x, y + 1] + temperature[x, y - 1] -
                4 * temperature[x, y]
            )
    return new_temperature

# Simulation loop
plt.ion()
for t in range(n_iter):
    temperature = update_temperature(temperature)

    if t % 10 == 0:  # Visualize every 10 iterations
        plt.clf()
        plt.imshow(temperature, cmap="hot", origin="lower")
        plt.colorbar(label="Temperature")
        plt.title(f"Heat Diffusion at Iteration {t}")
        plt.pause(0.1)

plt.ioff()
plt.show()
