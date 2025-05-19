import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orca Interaction Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Player class using orca image
class Player:
    def __init__(self):
        self.image = pygame.image.load("Orca.png").convert_alpha()  # Load the orca image
        self.image = pygame.transform.smoothscale(self.image, (80, 80))  # Smooth scaling for better quality
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 4
        self.score = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed

        # Prevent the player from moving out of bounds
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw(self):
        screen.blit(self.image, self.rect)

# Orca class (red circles)
class Orca:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = 10
        self.speed = 2

    def move_toward(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

    def distance_to(self, target):
        center_x = target.rect.centerx
        center_y = target.rect.centery
        return math.hypot(self.x - center_x, self.y - center_y)

# Fish class (green collectibles)
class Fish:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = 12  # Increased fish size for better visibility

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)

    def reposition(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)

# OPA logic
def opa_update(orca_list, player, iteration, max_iter):
    best_orca = min(orca_list, key=lambda o: o.distance_to(player))
    a = 2 * (1 - iteration / max_iter)

    for orca in orca_list:
        r = random.uniform(0, 1)
        D = abs(r * best_orca.x - orca.x)
        direction = -1 if random.random() < 0.5 else 1
        new_x = best_orca.x + direction * a * D

        D = abs(r * best_orca.y - orca.y)
        new_y = best_orca.y + direction * a * D

        orca.x = max(0, min(WIDTH, new_x))
        orca.y = max(0, min(HEIGHT, new_y))

# Game setup
player = Player()
orcas = [Orca() for _ in range(5)]
fish = Fish()
clock = pygame.time.Clock()
iteration = 0
max_iterations = 500

# Game loop
running = True
while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move(keys)
    opa_update(orcas, player, iteration, max_iterations)

    # Check for collecting fish
    if math.hypot(player.rect.centerx - fish.x, player.rect.centery - fish.y) < player.rect.width / 2 + fish.radius:
        player.score += 1
        fish.reposition()

    # Draw everything
    player.draw()
    fish.draw()
    for orca in orcas:
        orca.draw()

    # Draw score
    score_text = font.render(f"Score: {player.score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    iteration = min(iteration + 1, max_iterations)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
