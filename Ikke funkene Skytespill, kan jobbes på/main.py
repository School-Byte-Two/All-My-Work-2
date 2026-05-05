import random
import tkinter as tk
import time
import math

# -----------------------------------------------------------------------------
# SKYTESPILL - AVANSERT VERSJON
# En komplett 2D skytespill med bølger, oppgraderinger, fiender fra alle sider,
# rotasjon av spiller, eksplosjoner, partikler og mye mer!
# Skrevet i ren Python med Tkinter.
# -----------------------------------------------------------------------------

WIDTH = 960
HEIGHT = 720
FPS = 60
PLAYER_BASE_SPEED = 8
BULLET_BASE_SPEED = 18
ENEMY_BASE_SPEED = 3.5
SPAWN_INTERVAL = 1100
MAX_HEALTH = 100
WAVE_ENEMIES = 8
UPGRADE_CHOICES = 3

# Farger
BG_COLOR = "#0a0e1a"
PLAYER_COLOR = "#2eb8ff"
PLAYER_OUTLINE = "#a0d8ff"
BULLET_COLOR = "#ffea5f"
ENEMY_COLORS = ["#ff6262", "#ff9a4d", "#ff4dd4", "#62ff62", "#4d9aff"]
EXPLOSION_COLORS = ["#ffaa00", "#ff6600", "#ff3300", "#ff0000"]
PARTICLE_COLORS = ["#ffffff", "#ffff88", "#88ffff", "#ff88ff"]
HUD_COLOR = "#e0f0ff"
TITLE_COLOR = "#c0d8ff"
BUTTON_COLOR = "#4a90e2"
BUTTON_HOVER = "#5ba0f2"

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def length(self):
        return math.hypot(self.x, self.y)

    def normalized(self):
        l = self.length()
        return Vector(self.x / l, self.y / l) if l > 0 else Vector(0, 0)

    def rotate(self, angle):
        rad = math.radians(angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        return Vector(self.x * cos - self.y * sin, self.x * sin + self.y * cos)

class Actor:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.alive = True
        self.velocity = Vector(0, 0)

    def collides_with(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = (dx * dx + dy * dy) ** 0.5
        return distance < self.size + other.size

    def update_position(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

class Player(Actor):
    def __init__(self):
        super().__init__(WIDTH // 2, HEIGHT // 2, 28)
        self.health = MAX_HEALTH
        self.max_health = MAX_HEALTH
        self.score = 0
        self.cooldown = 0
        self.speed = PLAYER_BASE_SPEED
        self.angle = 0  # Rotasjon i grader
        self.last_move = Vector(0, 0)
        self.weapon_level = 1
        self.weapon_type = "normal"  # normal, explosive, multi
        self.shield = 0
        self.invincible_timer = 0

    def update(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.cooldown > 0:
            self.cooldown -= 1

    def move(self, dx, dy):
        self.last_move = Vector(dx, dy)
        if self.last_move.length() > 0:
            self.angle = math.degrees(math.atan2(dy, dx))
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(self.size, min(WIDTH - self.size, self.x))
        self.y = max(self.size, min(HEIGHT - self.size, self.y))

    def can_shoot(self):
        return self.cooldown <= 0

    def shoot(self):
        self.cooldown = max(5, 15 - self.weapon_level)
        bullets = []
        if self.weapon_type == "normal":
            bullets.append(Bullet(self.x, self.y, self.angle, BULLET_BASE_SPEED + self.weapon_level * 2))
        elif self.weapon_type == "multi":
            for i in range(3 + self.weapon_level):
                angle = self.angle + (i - (3 + self.weapon_level) // 2) * 15
                bullets.append(Bullet(self.x, self.y, angle, BULLET_BASE_SPEED + self.weapon_level * 2))
        elif self.weapon_type == "explosive":
            bullets.append(ExplosiveBullet(self.x, self.y, self.angle, BULLET_BASE_SPEED + self.weapon_level * 2, self.weapon_level))
        return bullets

    def take_damage(self, damage):
        if self.invincible_timer <= 0:
            if self.shield > 0:
                self.shield = max(0, self.shield - damage)
            else:
                self.health -= damage
                self.invincible_timer = 30  # Kort invincibility
            return True
        return False

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

class Bullet(Actor):
    def __init__(self, x, y, angle, speed):
        super().__init__(x, y, 6)
        self.angle = angle
        self.speed = speed
        self.velocity = Vector(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * speed
        self.damage = 1

    def update(self):
        self.update_position()
        if self.x < -20 or self.x > WIDTH + 20 or self.y < -20 or self.y > HEIGHT + 20:
            self.alive = False

class ExplosiveBullet(Bullet):
    def __init__(self, x, y, angle, speed, level):
        super().__init__(x, y, angle, speed)
        self.size = 8
        self.damage = 2 + level
        self.explosion_radius = 40 + level * 10

    def explode(self, game):
        # Lag eksplosjon og skade nærliggende fiender
        game.explosions.append(Explosion(self.x, self.y, self.explosion_radius))
        for enemy in game.enemies:
            if enemy.alive and self.collides_with(enemy):
                enemy.take_damage(self.damage)

class Enemy(Actor):
    def __init__(self, x, y, speed, size, health, color, enemy_type="normal"):
        super().__init__(x, y, size)
        self.speed = speed
        self.health = health
        self.max_health = health
        self.color = color
        self.enemy_type = enemy_type
        self.angle = 0
        self.shoot_timer = random.randint(60, 120)
        self.wave_offset = random.random() * math.pi * 2

    def update(self, player_pos):
        if self.enemy_type == "normal":
            direction = (player_pos - Vector(self.x, self.y)).normalized()
            self.velocity = direction * self.speed
        elif self.enemy_type == "wavy":
            direction = (player_pos - Vector(self.x, self.y)).normalized()
            wave = math.sin(time.time() * 3 + self.wave_offset) * 2
            self.velocity = direction * self.speed + Vector(-direction.y, direction.x) * wave
        elif self.enemy_type == "circling":
            angle = math.atan2(player_pos.y - self.y, player_pos.x - self.x)
            distance = (player_pos - Vector(self.x, self.y)).length()
            if distance > 100:
                self.velocity = Vector(math.cos(angle), math.sin(angle)) * self.speed
            else:
                self.velocity = Vector(-math.sin(angle), math.cos(angle)) * self.speed
        elif self.enemy_type == "boss":
            self.velocity = Vector(math.cos(time.time()), math.sin(time.time())) * self.speed

        self.update_position()
        self.angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x))

        # Sjekk om utenfor skjerm
        if self.x < -50 or self.x > WIDTH + 50 or self.y < -50 or self.y > HEIGHT + 50:
            self.alive = False

        self.shoot_timer -= 1

    def can_shoot(self):
        return self.shoot_timer <= 0

    def shoot(self, player_pos):
        self.shoot_timer = random.randint(80, 150)
        direction = (player_pos - Vector(self.x, self.y)).normalized()
        angle = math.degrees(math.atan2(direction.y, direction.x))
        return EnemyBullet(self.x, self.y, angle, BULLET_BASE_SPEED - 5)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False

class EnemyBullet(Bullet):
    def __init__(self, x, y, angle, speed):
        super().__init__(x, y, angle, speed)
        self.size = 4
        self.damage = 1

class Explosion:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.max_radius = radius
        self.timer = 0
        self.duration = 20

    def update(self):
        self.timer += 1
        self.radius = self.max_radius * (1 - self.timer / self.duration)

    def is_done(self):
        return self.timer >= self.duration

class Particle:
    def __init__(self, x, y, velocity, color, lifetime):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime

    def update(self):
        self.update_position()
        self.lifetime -= 1
        self.velocity = self.velocity * 0.98  # Friksjon

    def is_alive(self):
        return self.lifetime > 0

class Powerup(Actor):
    def __init__(self, x, y, powerup_type):
        super().__init__(x, y, 16)
        self.type = powerup_type
        self.angle = 0

    def update(self):
        self.angle += 5
        self.y += 2
        if self.y > HEIGHT + 20:
            self.alive = False

class UpgradeChoice:
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Avansert Skytespill")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        self.player = Player()
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.explosions = []
        self.particles = []
        self.powerups = []
        self.keys = {"up": False, "down": False, "left": False, "right": False, "space": False, "w": False, "a": False, "s": False, "d": False}
        self.last_spawn = 0
        self.running = False
        self.game_state = "menu"
        self.wave = 0
        self.enemies_killed_this_wave = 0
        self.upgrade_choices = []
        self.selected_upgrade = -1

        self.canvas.bind_all("<KeyPress>", self.key_press)
        self.canvas.bind_all("<KeyRelease>", self.key_release)
        self.canvas.bind_all("<Button-1>", self.mouse_click)
        self.root.after(1000 // FPS, self.game_loop)

    def key_press(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = True
        if self.game_state == "menu" and key == "return":
            self.start_game()
        elif self.game_state == "game_over" and key == "return":
            self.start_game()
        elif self.game_state == "upgrade" and key in "123":
            self.select_upgrade(int(key) - 1)

    def key_release(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = False

    def mouse_click(self, event):
        if self.game_state == "upgrade":
            for i, choice in enumerate(self.upgrade_choices):
                x = WIDTH // 2 - 200 + i * 150
                y = HEIGHT // 2 + 50
                if x <= event.x <= x + 120 and y <= event.y <= y + 40:
                    self.select_upgrade(i)

    def start_game(self):
        self.player = Player()
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.explosions = []
        self.particles = []
        self.powerups = []
        self.last_spawn = 0
        self.running = True
        self.game_state = "playing"
        self.wave = 0
        self.enemies_killed_this_wave = 0
        self.next_wave()

    def next_wave(self):
        self.wave += 1
        self.enemies_killed_this_wave = 0
        enemy_count = WAVE_ENEMIES + self.wave * 2
        for _ in range(enemy_count):
            self.spawn_enemy()

    def spawn_enemy(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x = random.randint(0, WIDTH)
            y = -20
        elif side == "bottom":
            x = random.randint(0, WIDTH)
            y = HEIGHT + 20
        elif side == "left":
            x = -20
            y = random.randint(0, HEIGHT)
        else:  # right
            x = WIDTH + 20
            y = random.randint(0, HEIGHT)

        enemy_type = random.choice(["normal", "wavy", "circling"])
        if self.wave > 5 and random.random() < 0.1:
            enemy_type = "boss"
        size = 20 + random.randint(0, 10)
        health = 1 + self.wave // 3
        speed = ENEMY_BASE_SPEED + self.wave * 0.2
        color = random.choice(ENEMY_COLORS)
        self.enemies.append(Enemy(x, y, speed, size, health, color, enemy_type))

    def update(self):
        if self.game_state != "playing":
            return

        self.player.update()

        # Spillerbevegelse
        dx = dy = 0
        if self.keys["left"] or self.keys["a"]:
            dx -= 1
        if self.keys["right"] or self.keys["d"]:
            dx += 1
        if self.keys["up"] or self.keys["w"]:
            dy -= 1
        if self.keys["down"] or self.keys["s"]:
            dy += 1
        if dx != 0 or dy != 0:
            self.player.move(dx, dy)

        # Skyting
        if self.keys["space"] and self.player.can_shoot():
            self.bullets.extend(self.player.shoot())

        # Oppdater objekter
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.alive]

        for bullet in self.enemy_bullets:
            bullet.update()
        self.enemy_bullets = [b for b in self.enemy_bullets if b.alive]

        player_pos = Vector(self.player.x, self.player.y)
        for enemy in self.enemies:
            enemy.update(player_pos)
            if enemy.can_shoot():
                self.enemy_bullets.append(enemy.shoot(player_pos))
        self.enemies = [e for e in self.enemies if e.alive]

        for explosion in self.explosions:
            explosion.update()
        self.explosions = [e for e in self.explosions if not e.is_done()]

        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.is_alive()]

        for powerup in self.powerups:
            powerup.update()
        self.powerups = [p for p in self.powerups if p.alive]

        # Spawn fiender
        if len(self.enemies) < 5 + self.wave:
            self.spawn_enemy()

        # Kollisjoner
        self.check_collisions()

        # Sjekk bølge slutt
        if len(self.enemies) == 0 and self.enemies_killed_this_wave >= WAVE_ENEMIES + self.wave * 2:
            self.show_upgrade_screen()

        if self.player.health <= 0:
            self.game_state = "game_over"
            self.running = False

    def check_collisions(self):
        # Kuler mot fiender
        for bullet in list(self.bullets):
            for enemy in list(self.enemies):
                if bullet.alive and enemy.alive and bullet.collides_with(enemy):
                    bullet.alive = False
                    enemy.take_damage(bullet.damage)
                    if not enemy.alive:
                        self.enemies_killed_this_wave += 1
                        self.player.score += 100 + enemy.max_health * 10
                        self.spawn_particles(enemy.x, enemy.y, 8, enemy.color)
                        if random.random() < 0.15:
                            self.powerups.append(Powerup(enemy.x, enemy.y, random.choice(["health", "shield", "speed"])))
                    if isinstance(bullet, ExplosiveBullet):
                        bullet.explode(self)

        # Fiendekuler mot spiller
        for bullet in list(self.enemy_bullets):
            if bullet.alive and bullet.collides_with(self.player):
                bullet.alive = False
                self.player.take_damage(bullet.damage)

        # Fiender mot spiller
        for enemy in list(self.enemies):
            if enemy.alive and enemy.collides_with(self.player):
                enemy.alive = False
                self.player.take_damage(10)
                self.spawn_particles(enemy.x, enemy.y, 12, enemy.color)

        # Powerups mot spiller
        for powerup in list(self.powerups):
            if powerup.alive and powerup.collides_with(self.player):
                powerup.alive = False
                if powerup.type == "health":
                    self.player.heal(25)
                elif powerup.type == "shield":
                    self.player.shield = min(50, self.player.shield + 20)
                elif powerup.type == "speed":
                    self.player.speed = min(PLAYER_BASE_SPEED * 2, self.player.speed + 1)

    def spawn_particles(self, x, y, count, color):
        for _ in range(count):
            angle = random.random() * math.pi * 2
            speed = random.random() * 5 + 2
            velocity = Vector(math.cos(angle), math.sin(angle)) * speed
            self.particles.append(Particle(x, y, velocity, color, random.randint(20, 40)))

    def show_upgrade_screen(self):
        self.game_state = "upgrade"
        self.upgrade_choices = [
            UpgradeChoice("Mer Helse", f"Øk maks helse med 20 (nå {self.player.max_health})",
                          lambda: setattr(self.player, 'max_health', self.player.max_health + 20)),
            UpgradeChoice("Bedre Våpen", f"Øk våpennivå (nå {self.player.weapon_level})",
                          lambda: setattr(self.player, 'weapon_level', min(10, self.player.weapon_level + 1))),
            UpgradeChoice("Mer Fart", f"Øk hastighet (nå {self.player.speed:.1f})",
                          lambda: setattr(self.player, 'speed', min(PLAYER_BASE_SPEED * 2, self.player.speed + 1))),
        ]
        if self.player.weapon_level >= 3 and random.random() < 0.3:
            self.upgrade_choices.append(
                UpgradeChoice("Nytt Våpen", "Bytt til nytt våpen (eksplosiv eller multi)",
                              lambda: self.upgrade_weapon())
            )

    def upgrade_weapon(self):
        if self.player.weapon_type == "normal":
            self.player.weapon_type = random.choice(["explosive", "multi"])
        elif self.player.weapon_type == "explosive":
            self.player.weapon_type = "multi"
        else:
            self.player.weapon_type = "explosive"

    def select_upgrade(self, index):
        if 0 <= index < len(self.upgrade_choices):
            self.upgrade_choices[index].effect()
            self.game_state = "playing"
            self.next_wave()

    def draw(self):
        self.canvas.delete("all")
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_playfield()
        elif self.game_state == "upgrade":
            self.draw_upgrade_screen()
        elif self.game_state == "game_over":
            self.draw_game_over()

    def draw_menu(self):
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 100, text="AVANSERT SKYTESPILL", fill=TITLE_COLOR, font=("Arial", 48, "bold"))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20, text="Trykk ENTER for å starte", fill=HUD_COLOR, font=("Arial", 24))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 30, text="Bruk WASD eller piltaster for å bevege, mellomrom for å skyte", fill=HUD_COLOR, font=("Arial", 18))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 60, text="Fiender kommer fra alle sider! Velg oppgraderinger mellom bølger!", fill=HUD_COLOR, font=("Arial", 16))

    def draw_playfield(self):
        # Tegn partikler
        for particle in self.particles:
            alpha = int(255 * (particle.lifetime / particle.max_lifetime))
            color = self.adjust_color_alpha(particle.color, alpha)
            self.canvas.create_oval(particle.x - 2, particle.y - 2, particle.x + 2, particle.y + 2, fill=color, outline="")

        # Tegn eksplosjoner
        for explosion in self.explosions:
            alpha = int(255 * (1 - explosion.timer / explosion.duration))
            color = self.adjust_color_alpha("#ffaa00", alpha)
            self.canvas.create_oval(explosion.x - explosion.radius, explosion.y - explosion.radius,
                                   explosion.x + explosion.radius, explosion.y + explosion.radius,
                                   fill="", outline=color, width=3)

        # Tegn powerups
        for powerup in self.powerups:
            self.canvas.create_oval(powerup.x - powerup.size, powerup.y - powerup.size,
                                   powerup.x + powerup.size, powerup.y + powerup.size,
                                   fill="#90ff90", outline="#ffffff", width=2)
            self.canvas.create_text(powerup.x, powerup.y, text=powerup.type[0].upper(), fill=BG_COLOR, font=("Arial", 12, "bold"))

        # Tegn kuler
        for bullet in self.bullets + self.enemy_bullets:
            color = BULLET_COLOR if bullet in self.bullets else "#ff8888"
            self.canvas.create_oval(bullet.x - bullet.size, bullet.y - bullet.size,
                                   bullet.x + bullet.size, bullet.y + bullet.size, fill=color, outline="")

        # Tegn fiender
        for enemy in self.enemies:
            self.canvas.create_oval(enemy.x - enemy.size, enemy.y - enemy.size,
                                   enemy.x + enemy.size, enemy.y + enemy.size,
                                   fill=enemy.color, outline="#ffffff", width=2)
            if enemy.health > 1:
                self.canvas.create_text(enemy.x, enemy.y, text=str(enemy.health), fill="#ffffff", font=("Arial", 10, "bold"))

        # Tegn spiller
        self.canvas.create_oval(self.player.x - self.player.size, self.player.y - self.player.size,
                               self.player.x + self.player.size, self.player.y + self.player.size,
                               fill=PLAYER_COLOR, outline=PLAYER_OUTLINE, width=3)
        nose = Vector(math.cos(math.radians(self.player.angle)), math.sin(math.radians(self.player.angle))) * self.player.size
        self.canvas.create_line(self.player.x, self.player.y,
                               self.player.x + nose.x, self.player.y + nose.y,
                               fill="#ffffff", width=3)
        if self.player.shield > 0:
            self.canvas.create_oval(self.player.x - self.player.size - 8, self.player.y - self.player.size - 8,
                                   self.player.x + self.player.size + 8, self.player.y + self.player.size + 8,
                                   outline="#87ceeb", width=4)

        # HUD
        self.canvas.create_text(20, 20, anchor="nw", text=f"Poeng: {self.player.score}", fill=HUD_COLOR, font=("Arial", 16, "bold"))
        self.canvas.create_text(20, 45, anchor="nw", text=f"Helse: {self.player.health}/{self.player.max_health}", fill=HUD_COLOR, font=("Arial", 16, "bold"))
        self.canvas.create_text(20, 70, anchor="nw", text=f"Bølge: {self.wave}", fill=HUD_COLOR, font=("Arial", 16, "bold"))
        self.canvas.create_text(20, 95, anchor="nw", text=f"Våpen: {self.player.weapon_type} (Lv.{self.player.weapon_level})", fill=HUD_COLOR, font=("Arial", 14))
        if self.player.shield > 0:
            self.canvas.create_text(20, 120, anchor="nw", text=f"Skjold: {self.player.shield}", fill=HUD_COLOR, font=("Arial", 14))

    def draw_upgrade_screen(self):
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 100, text=f"Bølge {self.wave} Fullført!", fill=TITLE_COLOR, font=("Arial", 36, "bold"))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 60, text="Velg en oppgradering:", fill=HUD_COLOR, font=("Arial", 24))

        for i, choice in enumerate(self.upgrade_choices):
            x = WIDTH // 2 - 200 + i * 150
            y = HEIGHT // 2 + 50
            self.canvas.create_rectangle(x, y, x + 120, y + 40, fill=BUTTON_COLOR, outline=BUTTON_HOVER, width=2)
            self.canvas.create_text(x + 60, y + 10, text=f"{i+1}. {choice.name}", fill="#ffffff", font=("Arial", 12, "bold"))
            self.canvas.create_text(x + 60, y + 25, text=choice.description, fill="#ffffff", font=("Arial", 10))

    def draw_game_over(self):
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 60, text="SPILLET ER SLUTT", fill="#ff6666", font=("Arial", 48, "bold"))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"Poeng: {self.player.score}", fill="#ffffff", font=("Arial", 24))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 40, text=f"Bølger overlevd: {self.wave}", fill="#ffffff", font=("Arial", 20))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 80, text="Trykk ENTER for ny runde", fill=HUD_COLOR, font=("Arial", 18))

    def adjust_color_alpha(self, color, alpha):
        # Enkel alpha-justering for farger (Tkinter støtter ikke alpha direkte)
        return color  # For enkelhet, returner original farge

    def game_loop(self):
        self.update()
        self.draw()
        self.root.after(1000 // FPS, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
