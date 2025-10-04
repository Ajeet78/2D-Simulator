import math
from constants import DEFAULT_MASS, DEFAULT_RADIUS, WHITE

class Particle:
    def __init__(self, x, y, vx=0, vy=0, mass=DEFAULT_MASS, radius=DEFAULT_RADIUS, color=WHITE):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radius = radius
        self.color = color
        self.fx = 0  # Accumulated force x
        self.fy = 0  # Accumulated force y

    def reset_force(self):
        self.fx = 0
        self.fy = 0

    def apply_force(self, fx, fy):
        self.fx += fx
        self.fy += fy

    def update(self, dt):
        # F = ma => a = F/m
        ax = self.fx / self.mass
        ay = self.fy / self.mass
        # Update velocity
        self.vx += ax * dt
        self.vy += ay * dt
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)

    def collides_with(self, other):
        dist = self.distance_to(other)
        return dist < self.radius + other.radius

    def merge_with(self, other):
        # Conservation of momentum
        total_mass = self.mass + other.mass
        self.vx = (self.vx * self.mass + other.vx * other.mass) / total_mass
        self.vy = (self.vy * self.mass + other.vy * other.mass) / total_mass
        self.mass = total_mass
        self.radius = math.sqrt(self.radius**2 + other.radius**2)  # Approximate volume conservation
        # Position: center of mass
        self.x = (self.x * self.mass + other.x * other.mass) / total_mass
        self.y = (self.y * self.mass + other.y * other.mass) / total_mass

    def elastic_collide(self, other):
        # Simple elastic collision for 2D
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist == 0:
            return  # Avoid division by zero
        nx = dx / dist
        ny = dy / dist

        # Relative velocity
        dvx = other.vx - self.vx
        dvy = other.vy - self.vy

        # Impulse
        impulse = 2 * (dvx * nx + dvy * ny) / (1/self.mass + 1/other.mass)
        self.vx += impulse * nx / self.mass
        self.vy += impulse * ny / self.mass
        other.vx -= impulse * nx / other.mass
        other.vy -= impulse * ny / other.mass

    def inelastic_collide(self, other, restitution=0.5):
        # Inelastic with energy loss
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist == 0:
            return
        nx = dx / dist
        ny = dy / dist

        dvx = other.vx - self.vx
        dvy = other.vy - self.vy

        impulse = (1 + restitution) * (dvx * nx + dvy * ny) / (1/self.mass + 1/other.mass)
        self.vx += impulse * nx / self.mass
        self.vy += impulse * ny / self.mass
        other.vx -= impulse * nx / other.mass
        other.vy -= impulse * ny / other.mass
