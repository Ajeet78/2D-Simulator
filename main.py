
import pygame
import sys
import time
from constants import WIDTH, HEIGHT, FPS, DT, BLACK, WHITE, RED, GREEN, BLUE, ELASTIC, MERGE, INELASTIC
from particle import Particle
from physics import calculate_forces, handle_collisions, generate_particles, update_particles
from gui import GUI

class Camera:
    def __init__(self, x=0, y=0, zoom=1.0):
        self.x = x
        self.y = y
        self.zoom = zoom

    def world_to_screen(self, wx, wy):
        sx = (wx - self.x) * self.zoom + WIDTH / 2
        sy = (wy - self.y) * self.zoom + HEIGHT / 2
        return sx, sy

    def screen_to_world(self, sx, sy):
        wx = (sx - WIDTH / 2) / self.zoom + self.x
        wy = (sy - HEIGHT / 2) / self.zoom + self.y
        return wx, wy

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("2D N-Body Particle Simulation")
    clock = pygame.time.Clock()

    MAX_PHYSICS_TIME = 0.016  # Don't block longer than 16ms

    particles = []
    camera = Camera()
    camera.x = WIDTH / 2
    camera.y = HEIGHT / 2
    gui = GUI()

    # Modes
    spawning = False
    deleting = False
    dragging = False
    last_mouse_pos = (0, 0)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Actual dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # Adjust GUI if needed, but for simplicity, keep fixed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    button_idx = gui.check_buttons(pos)
                    if button_idx == 0:  # Spawn
                        spawning = True
                    elif button_idx == 1:  # Delete
                        deleting = True
                    elif button_idx == 2:  # Clear
                        particles.clear()
                    elif button_idx == 3:  # 100
                        particles.extend(generate_particles(100))
                    elif button_idx == 4:  # 500
                        particles.extend(generate_particles(500))
                    elif button_idx == 5:  # 1000
                        particles.extend(generate_particles(1000))
                    elif button_idx == 6:  # 10000
                        particles.extend(generate_particles(10000))
                    elif button_idx == 7:  # Elastic
                        gui.collision_mode = ELASTIC
                    elif button_idx == 8:  # Merge
                        gui.collision_mode = MERGE
                    elif button_idx == 9:  # Inelastic
                        gui.collision_mode = INELASTIC
                    else:
                        if spawning:
                            wx, wy = camera.screen_to_world(*pos)
                            particles.append(Particle(wx, wy))
                            spawning = False
                        elif deleting:
                            wx, wy = camera.screen_to_world(*pos)
                            for p in particles[:]:
                                if (p.x - wx)**2 + (p.y - wy)**2 < p.radius**2:
                                    particles.remove(p)
                                    break
                            deleting = False
                        else:
                            dragging = True
                            last_mouse_pos = pos
                elif event.button == 3:  # Right click for pan
                    dragging = True
                    last_mouse_pos = event.pos
                elif event.button == 4:  # Wheel up zoom in
                    camera.zoom *= 1.1
                elif event.button == 5:  # Wheel down zoom out
                    camera.zoom /= 1.1
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dx = event.pos[0] - last_mouse_pos[0]
                    dy = event.pos[1] - last_mouse_pos[1]
                    camera.x -= dx / camera.zoom
                    camera.y -= dy / camera.zoom
                    last_mouse_pos = event.pos
            gui.handle_event(event)

        # Update camera zoom from slider
        camera.zoom = gui.get_zoom()

        # Physics with time budget to prevent freezing
        calculate_forces(particles, use_barnes_hut=True, time_limit=MAX_PHYSICS_TIME)
        update_particles(particles, DT)
        handle_collisions(particles, gui.collision_mode, time_limit=MAX_PHYSICS_TIME)

        # Render
        screen.fill(BLACK)

        # Draw particles
        for p in particles:
            sx, sy = camera.world_to_screen(p.x, p.y)
            radius = p.radius * camera.zoom
            if radius > 0.5 and 0 <= sx < WIDTH and 0 <= sy < HEIGHT:  # Only draw if on screen
                pygame.draw.circle(screen, p.color, (int(sx), int(sy)), int(radius))

        # Draw GUI
        gui.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
