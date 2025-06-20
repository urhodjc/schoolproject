import pygame
import random
import sys
import os
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 920, 800
GRID_SIZE = 40
BASE_FPS = 30
MAX_FPS = 120
FPS_INCREMENT = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 200, 100)  # Safe zone color
GRAY = (100, 100, 100)
RED = (200, 50, 50)
BLUE = (0, 100, 255)   # Portal color
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crossy Road Clone")
clock = pygame.time.Clock()

# Game variables
score = 0
high_score = 0
game_over = False
move_cooldown = 0  # To prevent continuous movement
current_fps = BASE_FPS

# Load high score from file if it exists
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            try:
                return int(file.read())
            except:
                return 0
    return 0

# Save high score to file
def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

high_score = load_high_score()

# Enhanced Player (chicken) with better graphics
class Player:
    def __init__(self):
        self.reset_position()
        self.width = GRID_SIZE * 0.9  # Slightly smaller than grid
        self.height = GRID_SIZE * 0.9
        self.speed = GRID_SIZE
        # New chicken colors
        self.body_color = (255, 220, 150)  # Light yellow body
        self.wing_color = (255, 200, 120)  # Slightly darker wings
        self.beak_color = (255, 180, 50)   # Orange beak
        self.feet_color = (255, 200, 0)    # Yellow feet
        self.comb_color = (255, 50, 50)    # Red comb
        self.can_move = True
        self.wing_flap = 0  # Animation counter
        self.head_bob = 0   # New head bobbing animation
    
    def reset_position(self):
        self.x = WIDTH // 2.1
        self.y = HEIGHT - GRID_SIZE * 2
    
    def draw(self):
        # Head bobbing animation
        self.head_bob = (self.head_bob + 0.05) % 6.28
        head_offset = math.sin(self.head_bob) * 2
        
        # Body (main oval)
        pygame.draw.ellipse(screen, self.body_color,
                          (self.x + self.width//4, self.y + self.height//4,
                           self.width//1.8, self.height//1.2))
        
        # Head (circle with bobbing effect)
        head_radius = self.width//3.5
        head_x = self.x + self.width//2
        head_y = self.y + head_radius//2 - head_offset
        pygame.draw.circle(screen, self.body_color, (head_x, head_y), head_radius)
        
        # Eyes (with cute white reflection)
        eye_radius = head_radius//4
        pygame.draw.circle(screen, BLACK, 
                         (head_x + head_radius//3, head_y - head_radius//6), 
                         eye_radius)
        pygame.draw.circle(screen, WHITE,
                         (head_x + head_radius//3 + 2, head_y - head_radius//6 - 2),
                         eye_radius//3)
        
        # Beak (triangle with shading)
        beak_points = [
            (head_x + head_radius//1.5, head_y),
            (head_x + head_radius//1.5 + head_radius//2, head_y - head_radius//4),
            (head_x + head_radius//1.5 + head_radius//2, head_y + head_radius//4)
        ]
        pygame.draw.polygon(screen, self.beak_color, beak_points)
        pygame.draw.polygon(screen, (255, 160, 40), beak_points, 1)  # Beak outline
        
        # Comb (more feather-like)
        comb_height = head_radius//1.5
        for i in range(3):  # Three comb points
            comb_width = head_radius//(2 + i/2)
            pygame.draw.polygon(screen, self.comb_color, [
                (head_x - head_radius//2 + i*head_radius//3, head_y - head_radius),
                (head_x - head_radius//3 + i*head_radius//3, head_y - head_radius - comb_height),
                (head_x - head_radius//3 + i*head_radius//3 + comb_width, head_y - head_radius)
            ])
        
        # Wings (animated flapping)
        self.wing_flap = (self.wing_flap + 0.1) % 6.28
        flap_offset = math.sin(self.wing_flap) * 4
        
        # Left wing (three feathers)
        for i in range(3):
            wing_length = self.width//(2 + i/3)
            pygame.draw.ellipse(screen, self.wing_color,
                              (self.x + self.width//6 - i*2, 
                               self.y + self.height//3 + flap_offset + i*3,
                               wing_length, self.height//4))
        
        # Right wing (mirrored)
        for i in range(3):
            wing_length = self.width//(2 + i/3)
            pygame.draw.ellipse(screen, self.wing_color,
                              (self.x + 2*self.width//3 + i*2, 
                               self.y + self.height//3 + flap_offset + i*3,
                               wing_length, self.height//4))
        
        # Tail feathers (three distinct feathers)
        tail_length = self.width//2
        for i in range(3):
            angle = -30 + i*30  # Spread out feathers
            feather_x = self.x + self.width//2 + math.cos(math.radians(angle)) * tail_length//2
            feather_y = self.y + self.height//1.2 + math.sin(math.radians(angle)) * tail_length//3
            pygame.draw.ellipse(screen, self.wing_color,
                              (feather_x - tail_length//4, feather_y - self.height//8,
                               tail_length//2, self.height//4))
        
        # Feet (two toes forward, one back)
        foot_y = self.y + self.height
        # Left foot
        pygame.draw.line(screen, self.feet_color,
                       (self.x + self.width//3, foot_y),
                       (self.x + self.width//3 - self.width//6, foot_y + self.height//4), 3)
        pygame.draw.line(screen, self.feet_color,
                       (self.x + self.width//3, foot_y),
                       (self.x + self.width//3 + self.width//8, foot_y + self.height//4), 3)
        pygame.draw.line(screen, self.feet_color,
                       (self.x + self.width//3, foot_y),
                       (self.x + self.width//3, foot_y + self.height//5), 3)  # Back toe
        
        # Right foot
        pygame.draw.line(screen, self.feet_color,
                       (self.x + 2*self.width//3, foot_y),
                       (self.x + 2*self.width//3 - self.width//6, foot_y + self.height//4), 3)
        pygame.draw.line(screen, self.feet_color,
                       (self.x + 2*self.width//3, foot_y),
                       (self.x + 2*self.width//3 + self.width//8, foot_y + self.height//4), 3)
        pygame.draw.line(screen, self.feet_color,
                       (self.x + 2*self.width//3, foot_y),
                       (self.x + 2*self.width//3, foot_y + self.height//5), 3)  # Back toe
    
    def move(self, dx, dy):
        if not self.can_move:
            return
            
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Boundary checking for x-axis (wrap around)
        if new_x < 0:
            new_x = WIDTH - self.width
        elif new_x > WIDTH - self.width:
            new_x = 0
            
        # Boundary checking for y-axis (teleport through portal at top)
        if new_y < 0:  # Reached top portal
            global current_fps
            current_fps = min(current_fps + FPS_INCREMENT, MAX_FPS)  # Increase FPS but cap at 120
            self.reset_position()  # Teleport back to safe zone
            return
            
        # Block downward movement at safe zone bottom
        if new_y > HEIGHT - GRID_SIZE * 2:
            new_y = HEIGHT - GRID_SIZE * 2
            
        self.x = new_x
        self.y = new_y
        
        # Score increases when moving up (but not when teleporting)
        if dy < 0 and new_y >= 0:  # Only increase if not teleporting
            global score, high_score
            score += 1
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            
        self.can_move = False  # Player must release key before moving again

# Enhanced Car class with better visuals
class Car:
    def __init__(self, x, y, width, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = GRID_SIZE - 5
        self.speed = speed
        self.color = self.generate_car_color()
        self.wheel_color = (40, 40, 40)
        self.window_color = (200, 230, 255)
        self.direction = 1 if speed > 0 else -1
    
    def generate_car_color(self):
        # More realistic car colors
        colors = [
            (200, 50, 50),    # Red
            (50, 50, 200),     # Blue
            (50, 200, 50),     # Green
            (200, 200, 50),    # Yellow
            (180, 180, 180),   # Silver
            (100, 50, 0)       # Brown
        ]
        return random.choice(colors)
    
    def draw(self):
        # Main car body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Car windows
        window_width = self.width // 3
        pygame.draw.rect(screen, self.window_color, 
                        (self.x + window_width//2, self.y + 5, window_width, self.height//3))
        pygame.draw.rect(screen, self.window_color, 
                        (self.x + self.width - window_width*1.2, self.y + 5, window_width, self.height//3))
        
        # Wheels
        wheel_radius = self.height // 4
        pygame.draw.circle(screen, self.wheel_color, 
                          (self.x + wheel_radius, self.y + self.height - wheel_radius//2), wheel_radius)
        pygame.draw.circle(screen, self.wheel_color, 
                          (self.x + self.width - wheel_radius, self.y + self.height - wheel_radius//2), wheel_radius)
        
        # Headlights/tail lights based on direction
        light_color = (255, 255, 200) if self.direction > 0 else (255, 100, 100)
        light_pos = self.x + (self.width if self.direction > 0 else 0)
        pygame.draw.rect(screen, light_color, (light_pos - 5, self.y + 5, 5, 5))
    
    def move(self):
        self.x += self.speed
        if self.speed > 0 and self.x > WIDTH:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = WIDTH

# Game objects
player = Player()
cars = []

# Define safe zone boundaries (3 rows at bottom)
SAFE_ZONE_TOP = HEIGHT - GRID_SIZE * 3  # Top of safe zone
SAFE_ZONE_BOTTOM = HEIGHT               # Bottom of screen

def generate_cars():
    global cars
    cars = []
    for i in range(-5, (HEIGHT - GRID_SIZE * 3) // GRID_SIZE):  # Stop before safe zone
        lane_y = i * GRID_SIZE
        if i % 2 == 1:  # Road lanes (only create above safe zone)
            # Add cars to this lane
            num_cars = random.randint(2, 4)
            direction = 1 if random.random() > 0.5 else -1
            speed = random.randint(2, 5) * direction
            
            for j in range(num_cars):
                car_width = random.randint(GRID_SIZE * 2, GRID_SIZE * 3)
                spacing = WIDTH // num_cars
                cars.append(Car(j * spacing + random.randint(0, spacing//2), 
                             lane_y + 2, 
                             car_width, 
                             speed))

# Create lanes and initial cars
lanes = []
for i in range(-5, (HEIGHT - GRID_SIZE * 3) // GRID_SIZE):  # Stop before safe zone
    lane_y = i * GRID_SIZE
    if i % 2 == 1:  # Road lanes
        lanes.append(("road", lane_y))
    else:  # Grass lanes
        lanes.append(("grass", lane_y))

# Add safe zone grass lanes at bottom
for i in range(4):  # Add 4 safe zone rows
    lanes.append(("safe_zone", HEIGHT - GRID_SIZE * (4 - i)))

# Generate initial cars
generate_cars()

# Enhanced Portal with animation
portal_frame = 0
portal_y = 0
portal_height = GRID_SIZE

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                # Reset game
                player = Player()
                score = 0
                game_over = False
                current_fps = BASE_FPS  # Reset FPS
                generate_cars()  # Regenerate cars
        
        # Reset movement flag when key is released
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                player.can_move = True
    
    if not game_over:
        # Handle player movement (only on key press, not hold)
        keys = pygame.key.get_pressed()
        if player.can_move:
            if keys[pygame.K_w]:
                player.move(0, -1)
            elif keys[pygame.K_s]:
                player.move(0, 1)
            elif keys[pygame.K_a]:
                player.move(-1, 0)
            elif keys[pygame.K_d]:
                player.move(1, 0)
        
        # Move cars
        for car in cars:
            car.move()
            
            # Collision detection (only outside safe zone)
            if (player.y < SAFE_ZONE_TOP and
                player.y < car.y + car.height and
                player.y + player.height > car.y and
                player.x < car.x + car.width and
                player.x + player.width > car.x):
                game_over = True
    
    # Draw everything
    screen.fill(BLACK)
    
    # Animate portal
    portal_frame = (portal_frame + 0.1) % 20
    # Draw portal at top with animation
    for i in range(0, WIDTH, 20):
        offset = math.sin(portal_frame + i/50) * 5
        pygame.draw.arc(screen, BLUE, (i-10, portal_y-5 + offset, 20, portal_height+10), 
                        0, 3.14, 3)
        pygame.draw.arc(screen, WHITE, (i-8, portal_y-3 + offset, 16, portal_height+6), 
                        0, 3.14, 2)
    
    # Draw all lanes
    for lane_type, y in lanes:
        if -GRID_SIZE <= y <= HEIGHT:  # Only draw visible lanes
            if lane_type == "grass":
                pygame.draw.rect(screen, GREEN, (0, y, WIDTH, GRID_SIZE))
            elif lane_type == "road":
                pygame.draw.rect(screen, GRAY, (0, y, WIDTH, GRID_SIZE))
                # Draw road markings
                for x in range(0, WIDTH, GRID_SIZE * 2):
                    pygame.draw.rect(screen, WHITE, (x, y + GRID_SIZE//2 - 2, GRID_SIZE, 4))
            elif lane_type == "safe_zone":
                pygame.draw.rect(screen, GREEN, (0, y, WIDTH, GRID_SIZE))
                # Draw safe zone pattern
                for x in range(0, WIDTH, GRID_SIZE):
                    pygame.draw.circle(screen, (150, 220, 150), (x + GRID_SIZE//2, y + GRID_SIZE//2), 5)
    
    # Draw cars (only visible ones)
    for car in cars:
        if -car.height <= car.y <= HEIGHT:  # Only draw visible cars
            car.draw()
    player.draw()
    
    # Draw score and high score
    font = pygame.font.SysFont('Arial', 28, bold=True)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))
    
    # Draw current FPS with warning color when high
    fps_color = WHITE if current_fps < 90 else (255, 100, 100)
    fps_text = font.render(f"Speed: {current_fps}", True, fps_color)
    screen.blit(fps_text, (WIDTH // 2 - fps_text.get_width() // 2, 10))
    
    # Draw game over screen
    if game_over:
        game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
    
    # Update display
    pygame.display.flip()
    clock.tick(current_fps)

pygame.quit()
sys.exit()