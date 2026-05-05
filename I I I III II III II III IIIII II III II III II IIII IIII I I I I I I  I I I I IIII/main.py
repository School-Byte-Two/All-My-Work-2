import pygame
import random
import os
import pickle
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Create simple sounds
arr_eat = np.array([[4000, 4000]] * 4410, dtype=np.int16)
eat_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(arr_eat))
arr_death = np.array([[2000, 2000]] * 4410, dtype=np.int16)
death_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(arr_death))
arr_powerup = np.array([[6000, 6000]] * 4410, dtype=np.int16)
powerup_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(arr_powerup))

# Constants
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
FPS = 10
INITIAL_SPEED = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)

# Directions
UP = (0, -BLOCK_SIZE)
DOWN = (0, BLOCK_SIZE)
LEFT = (-BLOCK_SIZE, 0)
RIGHT = (BLOCK_SIZE, 0)

class Snake:
    def __init__(self, game):
        self.game = game
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_snake(self):
        self.grow = True

    def draw(self, screen):
        alpha = 128 if self.game.invisible else 255
        for segment in self.body:
            s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            s.set_alpha(alpha)
            s.fill(GREEN)
            screen.blit(s, segment)

    def check_collision(self, obstacles):
        head = self.body[0]
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        if not self.game.invisible:  # Only check obstacles if not invisible
            for obs in obstacles:
                if head == obs:
                    return True
        return False

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

class PowerUp:
    def __init__(self):
        self.types = ['speed', 'shrink', 'points', 'teleport', 'slow', 'multi_food', 'invisible', 'shield', 'obstacle_clear']
        self.type = random.choice(self.types)
        self.position = self.random_position()
        self.timer = 0

    def random_position(self):
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return (x, y)

    def draw(self, screen):
        if self.type == 'speed':
            color = BLUE
        elif self.type == 'shrink':
            color = YELLOW
        elif self.type == 'points':
            color = PURPLE
        elif self.type == 'teleport':
            color = ORANGE
        elif self.type == 'slow':
            color = PINK
        elif self.type == 'multi_food':
            color = RED
        elif self.type == 'invisible':
            color = GRAY
        elif self.type == 'shield':
            color = (200, 200, 0)
        else:  # obstacle_clear
            color = (100, 200, 255)
        pygame.draw.rect(screen, color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 30  # frames

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / 30))
            color = (0, 255, 0, alpha) if alpha > 0 else (0, 255, 0)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 2)

class Projectile:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = 8

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y)), self.size)

    def is_out_of_bounds(self):
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT

class Boss:
    def __init__(self, game, level):
        self.game = game
        self.level = level
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        self.size = 25
        self.health = 3 + level
        self.max_health = self.health
        self.attack_timer = 60  # 6 seconds before first attack
        self.projectiles = []
        self.spike_timer = 0
        self.move_timer = 0
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def update(self):
        self.attack_timer -= 1
        self.spike_timer -= 1
        self.move_timer -= 1

        # Random movement
        if self.move_timer <= 0:
            self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
            self.move_timer = random.randint(30, 60)

        self.x += self.direction[0] * 0.5
        self.y += self.direction[1] * 0.5

        # Bounce off walls
        if self.x - self.size < 0 or self.x + self.size > WIDTH:
            self.direction = (self.direction[0] * -1, self.direction[1])
        if self.y - self.size < 0 or self.y + self.size > HEIGHT:
            self.direction = (self.direction[0], self.direction[1] * -1)

        # Attack
        if self.attack_timer <= 0:
            if random.random() < 0.5:
                self.shoot_projectiles()
            self.attack_timer = random.randint(60, 120)

        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update()
            if proj.is_out_of_bounds():
                self.projectiles.remove(proj)

    def shoot_projectiles(self):
        for angle in [0, 90, 180, 270]:
            rad = angle * 3.14159 / 180
            vx = 3 * np.cos(rad)
            vy = 3 * np.sin(rad)
            self.projectiles.append(Projectile(self.x, self.y, vx, vy))

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), self.size)
        # Draw health
        health_text = pygame.font.SysFont(None, 20).render(f"HP: {self.health}", True, WHITE)
        screen.blit(health_text, (int(self.x) - 20, int(self.y) - self.size - 20))

    def check_collision_with_snake(self, snake):
        for segment in snake.body:
            dist = ((self.x - segment[0]) ** 2 + (self.y - segment[1]) ** 2) ** 0.5
            if dist < self.size + BLOCK_SIZE // 2:
                self.health -= 1
                return True
        return False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Super Advanced Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.state = 'menu'
        self.snake = Snake(self)
        self.food = Food()
        self.extra_foods = []
        self.powerups = []
        self.obstacles = []
        self.particles = []
        self.boss = None
        self.projectiles = []
        self.score = 0
        self.level = 1
        self.speed = INITIAL_SPEED
        self.high_scores = self.load_high_score()
        self.high_score = self.high_scores[0] if self.high_scores else 0
        self.paused = False
        self.powerup_timer = 0
        self.invisible = False
        self.invisible_timer = 0
        self.shield = False
        self.shield_timer = 0

    def load_high_score(self):
        if os.path.exists('high_scores.pkl'):
            with open('high_scores.pkl', 'rb') as f:
                return pickle.load(f)
        return []

    def save_high_score(self):
        scores = self.load_high_score()
        scores.append(self.score)
        scores.sort(reverse=True)
        scores = scores[:5]  # Top 5
        with open('high_scores.pkl', 'wb') as f:
            pickle.dump(scores, f)
        self.high_scores = scores

    def reset_game(self):
        self.snake = Snake(self)
        self.food = Food()
        self.extra_foods = []
        self.powerups = []
        self.obstacles = []
        self.particles = []
        self.boss = None
        self.projectiles = []
        self.score = 0
        self.level = 1
        self.speed = INITIAL_SPEED
        self.paused = False
        self.powerup_timer = 0
        self.invisible = False
        self.invisible_timer = 0
        self.shield = False
        self.shield_timer = 0

    def add_obstacles(self):
        num_obstacles = self.level * 2  # More obstacles per level
        for _ in range(num_obstacles):
            pos = self.food.random_position()
            while pos in self.snake.body or pos == self.food.position:
                pos = self.food.random_position()
            self.obstacles.append(pos)

    def update(self):
        if self.state == 'playing' and not self.paused:
            self.snake.move()
            
            # Shield blocks obstacles once
            if self.shield_timer > 0:
                self.shield_timer -= 1
            else:
                self.shield = False
            
            if self.snake.check_collision(self.obstacles):
                if self.shield:
                    self.shield = False
                    self.obstacles = self.obstacles[1:] if self.obstacles else []
                else:
                    death_sound.play()
                    self.state = 'game_over'
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
                    return

            if self.snake.body[0] == self.food.position:
                eat_sound.play()
                self.snake.grow_snake()
                self.score += 10
                # Add particles
                for _ in range(5):
                    self.particles.append(Particle(self.food.position[0] + BLOCK_SIZE // 2, self.food.position[1] + BLOCK_SIZE // 2))
                self.food.position = self.food.random_position()
                if self.score % 50 == 0:
                    self.level += 1
                    self.speed += 2
                    self.add_obstacles()
                if random.random() < 0.5:  # 50% chance (doubled)
                    self.powerups.append(PowerUp())
            
            # Check if boss should spawn
            if self.score > 0 and self.score % 150 == 0 and self.boss is None:
                self.boss = Boss(self, self.score // 150)

            # Check extra foods
            for ef in self.extra_foods[:]:
                if self.snake.body[0] == ef.position:
                    eat_sound.play()
                    self.snake.grow_snake()
                    self.score += 10
                    # Add particles
                    for _ in range(5):
                        self.particles.append(Particle(ef.position[0] + BLOCK_SIZE // 2, ef.position[1] + BLOCK_SIZE // 2))
                    self.extra_foods.remove(ef)

            for pu in self.powerups[:]:
                if self.snake.body[0] == pu.position:
                    powerup_sound.play()
                    self.apply_powerup(pu)
                    self.powerups.remove(pu)

            # Update particles
            for p in self.particles[:]:
                p.update()
                if p.life <= 0:
                    self.particles.remove(p)

            # Update boss
            if self.boss:
                self.boss.update()
                # Check snake collision with boss
                if self.boss.check_collision_with_snake(self.snake):
                    for _ in range(3):
                        self.particles.append(Particle(self.boss.x, self.boss.y))
                # Check boss death
                if self.boss.health <= 0:
                    powerup_sound.play()
                    self.score += 100
                    # Spawn special power-up
                    special_pu = PowerUp()
                    special_pu.position = (self.boss.x, self.boss.y)
                    self.powerups.append(special_pu)
                    self.boss = None
                # Check projectile collisions with snake
                for proj in self.boss.projectiles[:]:
                    dist_to_head = ((proj.x - self.snake.body[0][0]) ** 2 + (proj.y - self.snake.body[0][1]) ** 2) ** 0.5
                    if dist_to_head < proj.size + BLOCK_SIZE // 2:
                        if self.shield:
                            self.shield = False
                            self.boss.projectiles.remove(proj)
                        elif not self.invisible:
                            death_sound.play()
                            self.state = 'game_over'
                            if self.score > self.high_score:
                                self.high_score = self.score
                                self.save_high_score()
                            return

            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.speed = INITIAL_SPEED + (self.level - 1) * 2

            self.invisible_timer -= 1
            if self.invisible_timer <= 0:
                self.invisible = False

    def apply_powerup(self, pu):
        if pu.type == 'speed':
            self.speed += 5
            self.powerup_timer = 100  # 10 seconds at 10 FPS
        elif pu.type == 'shrink':
            if len(self.snake.body) > 1:
                self.snake.body.pop()
        elif pu.type == 'points':
            self.score += 20
        elif pu.type == 'teleport':
            # Teleport to a safe position
            safe_pos = self.food.random_position()
            while safe_pos in self.snake.body or safe_pos in self.obstacles or safe_pos == self.food.position:
                safe_pos = self.food.random_position()
            self.snake.body[0] = safe_pos
        elif pu.type == 'slow':
            self.speed = max(5, self.speed - 5)
            self.powerup_timer = 100  # 10 seconds
        elif pu.type == 'multi_food':
            for _ in range(3):
                ef = Food()
                ef.position = ef.random_position()
                self.extra_foods.append(ef)
        elif pu.type == 'invisible':
            self.invisible = True
            self.invisible_timer = 150  # 15 seconds
        elif pu.type == 'shield':
            self.shield = True
            self.shield_timer = 200  # 20 seconds
        elif pu.type == 'obstacle_clear':
            self.obstacles = []

    def draw(self):
        self.screen.fill(BLACK)
        if self.state == 'menu':
            self.draw_menu()
        elif self.state == 'playing':
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            for ef in self.extra_foods:
                ef.draw(self.screen)
            for pu in self.powerups:
                pu.draw(self.screen)
            for obs in self.obstacles:
                pygame.draw.rect(self.screen, WHITE, (obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))
            for p in self.particles:
                p.draw(self.screen)
            if self.boss:
                self.boss.draw(self.screen)
                for proj in self.boss.projectiles:
                    proj.draw(self.screen)
            self.draw_score()
            if self.shield:
                shield_text = self.small_font.render("SHIELD", True, (200, 200, 0))
                self.screen.blit(shield_text, (WIDTH - 100, 10))
            if self.paused:
                self.draw_pause()
        elif self.state == 'game_over':
            self.draw_game_over()
        pygame.display.flip()

    def draw_menu(self):
        title = self.font.render("Super Advanced Snake", True, WHITE)
        start = self.small_font.render("Press SPACE to Start", True, WHITE)
        quit_text = self.small_font.render("Press Q to Quit", True, WHITE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2))
        self.screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 30))

    def draw_score(self):
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.small_font.render(f"Level: {self.level}", True, WHITE)
        high_text = self.small_font.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(high_text, (10, 70))

    def draw_pause(self):
        pause_text = self.font.render("Paused", True, WHITE)
        self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))

    def draw_game_over(self):
        over = self.font.render("Game Over", True, RED)
        score = self.small_font.render(f"Score: {self.score}", True, WHITE)
        high = self.small_font.render(f"High Score: {self.high_score}", True, WHITE)
        top_scores = [self.small_font.render(f"{i+1}. {s}", True, WHITE) for i, s in enumerate(self.high_scores)]
        restart = self.small_font.render("Press R to Restart", True, WHITE)
        quit_text = self.small_font.render("Press Q to Quit", True, WHITE)
        self.screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 80))
        self.screen.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(high, (WIDTH // 2 - high.get_width() // 2, HEIGHT // 2 - 20))
        for i, ts in enumerate(top_scores):
            self.screen.blit(ts, (WIDTH // 2 - ts.get_width() // 2, HEIGHT // 2 + 10 + i * 20))
        self.screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 120))
        self.screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 150))

    def handle_input(self, event):
        if self.state == 'menu':
            if event.key == pygame.K_SPACE:
                self.state = 'playing'
            elif event.key == pygame.K_q:
                pygame.quit()
                exit()
        elif self.state == 'playing':
            if event.key == pygame.K_UP and self.snake.direction != DOWN:
                self.snake.direction = UP
            elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                self.snake.direction = DOWN
            elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                self.snake.direction = LEFT
            elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                self.snake.direction = RIGHT
            elif event.key == pygame.K_p:
                self.paused = not self.paused
        elif self.state == 'game_over':
            if event.key == pygame.K_r:
                self.reset_game()
                self.state = 'playing'
            elif event.key == pygame.K_q:
                pygame.quit()
                exit()

def main():
    game = Game()
    running = True
    while running:
        game.clock.tick(game.speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.handle_input(event)
        game.update()
        game.draw()
    pygame.quit()

if __name__ == "__main__":
    main()