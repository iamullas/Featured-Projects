
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import G

# Define Earth's mass and an example asteroid's orbit parameters
earth_mass = 5.972e24  # kg
asteroid_mass = 1e12   # kg (hypothetical)
distance = np.linspace(6.5e6, 4e8, 100)  # Distance from Earth in meters

# Compute gravitational force
force = G * (earth_mass * asteroid_mass) / (distance**2)

# Plot the force as the asteroid moves closer to Earth
plt.figure(figsize=(8, 5))
plt.plot(distance / 1e6, force, label="Gravitational Force (N)", color='orange')
plt.xlabel("Distance from Earth (Million m)")
plt.ylabel("Force (N)")
plt.title("Asteroid Gravitational Force as It Approaches Earth")
plt.legend()
plt.grid()
plt.show()
