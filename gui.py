import pygame
from constants import WIDTH, HEIGHT, WHITE, BLACK, GRAY, GREEN, RED, BLUE

class Button:
    def __init__(self, x, y, w, h, text, color=WHITE, text_color=BLACK):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, label=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.font = pygame.font.SysFont(None, 24)
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        # Knob
        knob_x = self.rect.x + (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.w
        pygame.draw.circle(screen, RED, (int(knob_x), self.rect.centery), 10)
        # Label
        if self.label:
            label_surf = self.font.render(f"{self.label}: {int(self.val)}", True, BLACK)
            screen.blit(label_surf, (self.rect.x, self.rect.y - 30))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_val(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_val(event.pos[0])

    def update_val(self, mouse_x):
        rel_x = mouse_x - self.rect.x
        self.val = self.min_val + (rel_x / self.rect.w) * (self.max_val - self.min_val)
        self.val = max(self.min_val, min(self.max_val, self.val))

class GUI:
    def __init__(self):
        self.buttons = []
        self.sliders = []
        self.collision_mode = 0  # 0: Elastic, 1: Merge, 2: Inelastic
        self.setup_gui()

    def setup_gui(self):
        # Buttons
        self.buttons.append(Button(10, 10, 80, 30, "Spawn"))
        self.buttons.append(Button(100, 10, 80, 30, "Delete"))
        self.buttons.append(Button(190, 10, 80, 30, "Clear"))
        self.buttons.append(Button(10, 50, 80, 30, "100"))
        self.buttons.append(Button(100, 50, 80, 30, "500"))
        self.buttons.append(Button(190, 50, 80, 30, "1000"))
        self.buttons.append(Button(280, 50, 80, 30, "10000"))
        self.buttons.append(Button(10, 90, 80, 30, "Elastic"))
        self.buttons.append(Button(100, 90, 80, 30, "Merge"))
        self.buttons.append(Button(190, 90, 80, 30, "Inelastic"))

        # Sliders
        self.sliders.append(Slider(10, 130, 200, 20, 0.1, 2.0, 1.0, "Zoom"))

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)
        for slider in self.sliders:
            slider.draw(screen)

    def handle_event(self, event):
        for slider in self.sliders:
            slider.handle_event(event)

    def get_zoom(self):
        return self.sliders[0].val

    def check_buttons(self, pos):
        for i, button in enumerate(self.buttons):
            if button.is_clicked(pos):
                return i
        return -1
