import random
import time
from constants import G, SOFTENING, THETA, ELASTIC, MERGE, INELASTIC, WIDTH, HEIGHT
from quadtree import Quadtree, Rectangle
from particle import Particle

def build_quadtree(particles):
    # Find bounds
    if not particles:
        return Quadtree(Rectangle(0, 0, WIDTH, HEIGHT))
    min_x = min(p.x for p in particles)
    max_x = max(p.x for p in particles)
    min_y = min(p.y for p in particles)
    max_y = max(p.y for p in particles)
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    size = max(max_x - min_x, max_y - min_y) * 1.1  # Add margin
    boundary = Rectangle(center_x, center_y, size, size)
    qt = Quadtree(boundary)
    for p in particles:
        qt.insert(p)
    return qt

def calculate_forces(particles, use_barnes_hut=True, time_limit=None):
    start = time.time()
    if use_barnes_hut:
        qt = build_quadtree(particles)
        for p in particles:
            if time_limit and time.time() - start > time_limit:
                break
            p.reset_force()
            fx, fy = qt.calculate_force(p, THETA, G, SOFTENING)
            p.apply_force(fx, fy)
    else:
        # O(n^2) brute force
        for i, p1 in enumerate(particles):
            if time_limit and time.time() - start > time_limit:
                break
            p1.reset_force()
            for j, p2 in enumerate(particles):
                if i == j:
                    continue
                if time_limit and time.time() - start > time_limit:
                    break
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                dist_sq = dx*dx + dy*dy + SOFTENING
                dist = dist_sq ** 0.5
                force = G * p1.mass * p2.mass / dist_sq
                fx = force * dx / dist
                fy = force * dy / dist
                p1.apply_force(fx, fy)

def handle_collisions(particles, collision_mode, time_limit=None):
    start = time.time()
    to_remove = set()
    for i in range(len(particles)):
        if time_limit and time.time() - start > time_limit:
            break
        if particles[i] in to_remove:
            continue
        for j in range(i+1, len(particles)):
            if time_limit and time.time() - start > time_limit:
                break
            if particles[j] in to_remove:
                continue
            if particles[i].collides_with(particles[j]):
                if collision_mode == MERGE:
                    particles[i].merge_with(particles[j])
                    to_remove.add(particles[j])
                elif collision_mode == ELASTIC:
                    particles[i].elastic_collide(particles[j])
                elif collision_mode == INELASTIC:
                    particles[i].inelastic_collide(particles[j])
    # Remove merged particles
    particles[:] = [p for p in particles if p not in to_remove]

def generate_particles(count, center_x=WIDTH/2, center_y=HEIGHT/2, spread=100):
    particles = []
    for _ in range(count):
        x = center_x + random.uniform(-spread, spread)
        y = center_y + random.uniform(-spread, spread)
        vx = random.uniform(-50, 50)
        vy = random.uniform(-50, 50)
        mass = random.uniform(0.5, 2.0)
        radius = mass * 5  # Scale radius with mass
        particles.append(Particle(x, y, vx, vy, mass, radius))
    return particles

def update_particles(particles, dt):
    for p in particles:
        p.update(dt)
