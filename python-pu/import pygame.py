import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
GRID_SIZE = 40
FPS = 60

# Colors (expanded palette)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (50, 200, 50)  # Brighter green for grass
DARK_GREEN = (0, 100, 0)  # For grass details
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)  # Road color
LIGHT_GRAY = (100, 100, 100)  # Sidewalk
YELLOW = (255, 255, 0)  # Road markings
BROWN = (139, 69, 19)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crossy Road - Improved Graphics")
clock = pygame.time.Clock()

# Game variables
score = 0
game_over = False

# Player (chicken) with improved graphics
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - GRID_SIZE * 2
        self.width = GRID_SIZE
        self.height = GRID_SIZE
        self.speed = GRID_SIZE
    
    def draw(self):
        # Body
        pygame.draw.ellipse(screen, WHITE, (self.x, self.y, self.width, self.height))
        # Head
        pygame.draw.circle(screen, WHITE, (self.x + self.width//2, self.y - 5), 10)
        # Eyes
        pygame.draw.circle(screen, BLACK, (self.x + self.width//2 - 3, self.y - 7), 2)
        pygame.draw.circle(screen, BLACK, (self.x + self.width//2 + 3, self.y - 7), 2)
        # Beak
        pygame.draw.polygon(screen, (255, 200, 0), [
            (self.x + self.width//2, self.y - 3),
            (self.x + self.width//2 + 10, self.y),
            (self.x + self.width//2, self.y + 3)
        ])
        # Comb
        pygame.draw.polygon(screen, RED, [
            (self.x + self.width//2 - 5, self.y - 10),
            (self.x + self.width//2, self.y - 15),
            (self.x + self.width//2 + 5, self.y - 10)
        ])
        # Feet
        pygame.draw.line(screen, (255, 200, 0), (self.x + 10, self.y + self.height), (self.x + 15, self.y + self.height + 5), 2)
        pygame.draw.line(screen, (255, 200, 0), (self.x + self.width - 10, self.y + self.height), (self.x + self.width - 15, self.y + self.height + 5), 2)
    
    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Boundary checking
        if 0 <= new_x <= WIDTH - self.width:
            self.x = new_x
        if 0 <= new_y <= HEIGHT - self.height:
            self.y = new_y

# Cars with improved graphics
class Car:
    def __init__(self, y, speed):
        self.width = random.randint(GRID_SIZE * 2, GRID_SIZE * 3)
        self.height = GRID_SIZE
        self.x = -self.width if speed > 0 else WIDTH
        self.y = y
        self.speed = speed
        self.color = random.choice([(200, 0, 0), (0, 0, 200), (0, 200, 0), (100, 100, 100)])  # Darker colors
    
    def draw(self):
        # Main body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Windows
        window_color = (150, 200, 255)
        pygame.draw.rect(screen, window_color, (self.x + 5, self.y + 5, self.width//3, self.height - 10))
        pygame.draw.rect(screen, window_color, (self.x + self.width//3 + 10, self.y + 5, self.width//3, self.height - 10))
        # Wheels
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + self.height), 7)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 10, self.y + self.height), 7)
        # Lights
        light_color = (255, 255, 150) if self.speed > 0 else (255, 50, 50)
        pygame.draw.rect(screen, light_color, (self.x + (self.width - 10 if self.speed > 0 else 0), self.y + 15, 10, 5))
    
    def move(self):
        self.x += self.speed
        if self.speed > 0 and self.x > WIDTH:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = WIDTH

def draw_grass_area(rect):
    # Base grass color
    pygame.draw.rect(screen, GREEN, rect)
    # Grass details
    for x in range(0, rect.width, 5):
        for y in range(rect.y, rect.y + rect.height, 10):
            if random.random() > 0.7:  # Only draw some grass blades
                blade_x = rect.x + x + random.randint(-2, 2)
                blade_height = random.randint(3, 7)
                pygame.draw.line(screen, DARK_GREEN, 
                                (blade_x, y + random.randint(0, 5)),
                                (blade_x + random.randint(-2, 2), y - blade_height), 
                                1)

def draw_road():
    # Road surface
    for lane_y in range(HEIGHT - GRID_SIZE * 3, GRID_SIZE * 3, -GRID_SIZE * 2):
        pygame.draw.rect(screen, GRAY, (0, lane_y, WIDTH, GRID_SIZE))
        
        # Road markings (dashed lines)
        for mark_x in range(0, WIDTH, GRID_SIZE * 2):
            pygame.draw.rect(screen, YELLOW, (mark_x, lane_y + GRID_SIZE//2 - 2, GRID_SIZE, 4))
        
        # Sidewalk
        pygame.draw.rect(screen, LIGHT_GRAY, (0, lane_y - 3, WIDTH, 3))
        pygame.draw.rect(screen, LIGHT_GRAY, (0, lane_y + GRID_SIZE, WIDTH, 3))

def draw_score():
    font = pygame.font.SysFont('Arial', 28, bold=True)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def check_collision():
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for car in cars:
        car_rect = pygame.Rect(car.x, car.y, car.width, car.height)
        if player_rect.colliderect(car_rect):
            return True
    return False

def reset_game():
    global player, cars, score, game_over
    player = Player()
    score = 0
    game_over = False
    cars = []
    # Recreate lanes of cars
    for i in range(5):
        lane_y = HEIGHT - GRID_SIZE * (4 + i * 2)
        speed = random.choice([-3, -2, 2, 3])
        cars.append(Car(lane_y, speed))
        if random.random() > 0.5:
            cars.append(Car(lane_y, speed))

# Game objects
player = Player()
cars = []
safe_area = pygame.Rect(0, 0, WIDTH, GRID_SIZE * 3)  # Grass area at the top

# Create initial cars
for i in range(5):
    lane_y = HEIGHT - GRID_SIZE * (4 + i * 2)
    speed = random.choice([-3, -2, 2, 3])
    cars.append(Car(lane_y, speed))
    if random.random() > 0.5:
        cars.append(Car(lane_y, speed))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move(0, -1)
                if player.y < HEIGHT - GRID_SIZE * 6:
                    score += 1
            elif event.key == pygame.K_DOWN:
                player.move(0, 1)
            elif event.key == pygame.K_LEFT:
                player.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)
            elif event.key == pygame.K_r and game_over:
                reset_game()
    
    # Game logic
    if not game_over:
        for car in cars:
            car.move()
        
        # Check if player reached the safe area
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        if player_rect.colliderect(safe_area):
            score += 10
            player.y = HEIGHT - GRID_SIZE * 2  # Reset position
        
        # Check for collisions
        if check_collision():
            game_over = True
    
    # Drawing
    screen.fill(DARK_GREEN)  # Background color
    
    # Draw game elements
    draw_road()
    draw_grass_area(safe_area)
    
    for car in cars:
        car.draw()
    player.draw()
    
    draw_score()
    
    # Draw game over screen
    if game_over:
        # Semi-transparent overlay
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))  # Black with 50% opacity
        screen.blit(s, (0, 0))
        
        font = pygame.font.SysFont('Arial', 48, bold=True)
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        
        font = pygame.font.SysFont('Arial', 28)
        restart_text = font.render("Press R to restart", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()