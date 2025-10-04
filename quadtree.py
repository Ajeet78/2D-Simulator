import math

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, particle):
        return (particle.x >= self.x - self.w/2 and
                particle.x <= self.x + self.w/2 and
                particle.y >= self.y - self.h/2 and
                particle.y <= self.y + self.h/2)

    def intersects(self, range_rect):
        return not (range_rect.x - range_rect.w/2 > self.x + self.w/2 or
                    range_rect.x + range_rect.w/2 < self.x - self.w/2 or
                    range_rect.y - range_rect.h/2 > self.y + self.h/2 or
                    range_rect.y + range_rect.h/2 < self.y - self.h/2)

class Quadtree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.particles = []
        self.divided = False
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None
        self.total_mass = 0
        self.center_x = 0
        self.center_y = 0

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        nw = Rectangle(x - w/2, y - h/2, w, h)
        self.northwest = Quadtree(nw, self.capacity)
        ne = Rectangle(x + w/2, y - h/2, w, h)
        self.northeast = Quadtree(ne, self.capacity)
        sw = Rectangle(x - w/2, y + h/2, w, h)
        self.southwest = Quadtree(sw, self.capacity)
        se = Rectangle(x + w/2, y + h/2, w, h)
        self.southeast = Quadtree(se, self.capacity)
        self.divided = True

    def insert(self, particle):
        if not self.boundary.contains(particle):
            return False

        if len(self.particles) < self.capacity:
            self.particles.append(particle)
            self.update_center_of_mass(particle)
            return True
        else:
            if not self.divided:
                self.subdivide()
            if self.northwest.insert(particle):
                return True
            if self.northeast.insert(particle):
                return True
            if self.southwest.insert(particle):
                return True
            if self.southeast.insert(particle):
                return True
        return False

    def update_center_of_mass(self, particle):
        self.total_mass += particle.mass
        self.center_x = (self.center_x * (self.total_mass - particle.mass) + particle.x * particle.mass) / self.total_mass
        self.center_y = (self.center_y * (self.total_mass - particle.mass) + particle.y * particle.mass) / self.total_mass

    def query(self, range_rect, found=None):
        if found is None:
            found = []
        if not self.boundary.intersects(range_rect):
            return found
        for p in self.particles:
            if range_rect.contains(p):
                found.append(p)
        if self.divided:
            self.northwest.query(range_rect, found)
            self.northeast.query(range_rect, found)
            self.southwest.query(range_rect, found)
            self.southeast.query(range_rect, found)
        return found

    def calculate_force(self, particle, theta, G, softening):
        if self.total_mass == 0:
            return 0, 0

        dx = self.center_x - particle.x
        dy = self.center_y - particle.y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist == 0:
            return 0, 0

        if not self.divided or self.boundary.w / dist < theta:
            # Approximate as point mass
            force = G * self.total_mass * particle.mass / (dist*dist + softening)
            fx = force * dx / dist
            fy = force * dy / dist
            return fx, fy
        else:
            # Recurse
            fx = 0
            fy = 0
            if self.northwest:
                f = self.northwest.calculate_force(particle, theta, G, softening)
                fx += f[0]
                fy += f[1]
            if self.northeast:
                f = self.northeast.calculate_force(particle, theta, G, softening)
                fx += f[0]
                fy += f[1]
            if self.southwest:
                f = self.southwest.calculate_force(particle, theta, G, softening)
                fx += f[0]
                fy += f[1]
            if self.southeast:
                f = self.southeast.calculate_force(particle, theta, G, softening)
                fx += f[0]
                fy += f[1]
            return fx, fy
