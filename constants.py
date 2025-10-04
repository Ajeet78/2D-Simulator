import math

# Gravitational constant (scaled for simulation to avoid huge forces)
G = 6.67430e-11 * 1e-6

# Collision modes
ELASTIC = 0
MERGE = 1
INELASTIC = 2

# Default particle properties
DEFAULT_MASS = 1.0
DEFAULT_RADIUS = 5.0

# Simulation settings
DT = 0.016  # Time step (approx 60 FPS)
SOFTENING = 0.1  # Softening parameter for gravity

# Screen settings
WIDTH = 800
HEIGHT = 600
FPS = 60

# Camera settings
ZOOM_SPEED = 0.1
PAN_SPEED = 1.0
MIN_ZOOM = 0.1
MAX_ZOOM = 10.0

# Barnes-Hut theta
THETA = 0.5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
