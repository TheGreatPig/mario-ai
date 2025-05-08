import pygame
import sys

# Initialize Pygame
pygame.init()
SCALE = 3
SCREEN_WIDTH = 256 * SCALE
SCREEN_HEIGHT = 240 * SCALE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Bros. World 1-1 - Unchained")

# Colors (for placeholders)
SKY_BLUE = (92, 148, 252)
GROUND_BROWN = (139, 69, 19)
BLOCK_GRAY = (128, 128, 128)
COIN_YELLOW = (255, 255, 0)

# Constants
TILE_SIZE = 16 * SCALE
MARIO_WIDTH = 5 * SCALE
MARIO_HEIGHT = 18 * SCALE
WALK_SPEED = 2 * SCALE
RUN_SPEED = 4 * SCALE
JUMP_FORCE = -12.5 * SCALE  # Tweaked for NES feel
GRAVITY = 0.82 * SCALE
MAX_FALL_SPEED = 10 * SCALE
FRICTION = 0.85  # Momentum slide

# Level data (expanded World 1-1 chunk)
# 0 = sky, 1 = ground, 2 = brick, 3 = ?-block, 4 = pipe, 5 = coin
LEVEL = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Load sprites (uncomment and provide your own sprite files)
"""
try:
    MARIO_SPRITE = pygame.image.load("mario.png").convert_alpha()
    MARIO_SPRITE = pygame.transform.scale(MARIO_SPRITE, (MARIO_WIDTH, MARIO_HEIGHT))
    GOOMBA_SPRITE = pygame.image.load("goomba.png").convert_alpha()
    GOOMBA_SPRITE = pygame.transform.scale(GOOMBA_SPRITE, (16 * SCALE, 16 * SCALE))
    GROUND_TILE = pygame.image.load("ground.png").convert_alpha()
    GROUND_TILE = pygame.transform.scale(GROUND_TILE, (TILE_SIZE, TILE_SIZE))
    BRICK_TILE = pygame.image.load("brick.png").convert_alpha()
    BRICK_TILE = pygame.transform.scale(BRICK_TILE, (TILE_SIZE, TILE_SIZE))
    QBLOCK_TILE = pygame.image.load("qblock.png").convert_alpha()
    QBLOCK_TILE = pygame.transform.scale(QBLOCK_TILE, (TILE_SIZE, TILE_SIZE))
    PIPE_TILE = pygame.image.load("pipe.png").convert_alpha()
    PIPE_TILE = pygame.transform.scale(PIPE_TILE, (TILE_SIZE, TILE_SIZE))
    COIN_SPRITE = pygame.image.load("coin.png").convert_alpha()
    COIN_SPRITE = pygame.transform.scale(COIN_SPRITE, (16 * SCALE, 16 * SCALE))
except FileNotFoundError:
    print("Sprite files missing! Using placeholders.")
"""

# Mario class
class Mario:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, MARIO_WIDTH, MARIO_HEIGHT)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing_right = True
        self.running = False

    def update(self, keys, level, coins, goombas):
        # Horizontal movement
        self.running = keys[pygame.K_LSHIFT]
        target_vx = 0
        if keys[pygame.K_LEFT]:
            target_vx = -WALK_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            target_vx = WALK_SPEED
            self.facing_right = True
        if self.running and target_vx != 0:
            target_vx *= RUN_SPEED / WALK_SPEED

        # Apply momentum
        self.vx = self.vx * FRICTION + target_vx * (1 - FRICTION)

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False

        # Apply gravity
        self.vy += GRAVITY
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED

        # Update position
        self.rect.x += self.vx
        self.collide_x(level)
        self.rect.y += self.vy
        self.collide_y(level)

        # Check Goomba collisions
        for goomba in goombas[:]:
            if self.rect.colliderect(goomba.rect):
                if self.vy > 0 and self.rect.bottom - goomba.rect.top <= 10 * SCALE:
                    goombas.remove(goomba)  # Stomp Goomba
                    self.vy = -JUMP_FORCE / 2  # Bounce
                else:
                    print("Mario hit Goomba! Game over.")  # Placeholder death

        # Check coin collisions
        for coin in coins[:]:
            if self.rect.colliderect(coin.rect):
                coins.remove(coin)
                print("Coin collected!")

    def collide_x(self, level):
        for y in range(len(level)):
            for x in range(len(level[0])):
                if level[y][x] in [1, 2, 3, 4]:
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        if self.vx > 0:
                            self.rect.right = tile_rect.left
                        elif self.vx < 0:
                            self.rect.left = tile_rect.right
                        self.vx = 0

    def collide_y(self, level):
        self.on_ground = False
        for y in range(len(level)):
            for x in range(len(level[0])):
                if level[y][x] in [1, 2, 3, 4]:
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        if self.vy > 0:
                            self.rect.bottom = tile_rect.top
                            self.vy = 0
                            self.on_ground = True
                        elif self.vy < 0:
                            self.rect.top = tile_rect.bottom
                            self.vy = 0

    def draw(self, screen, camera_x):
        # Placeholder or sprite
        """
        if 'MARIO_SPRITE' in globals():
            sprite = MARIO_SPRITE
            if not self.facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            screen.blit(sprite, (self.rect.x - camera_x, self.rect.y))
        else:
        """
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x - camera_x, self.rect.y, MARIO_WIDTH, MARIO_HEIGHT))

# Goomba class
class Goomba:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 16 * SCALE, 16 * SCALE)
        self.vx = -1 * SCALE
        self.vy = 0
        self.on_ground = False

    def update(self, level):
        self.vy += GRAVITY
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED

        self.rect.x += self.vx
        self.collide_x(level)
        self.rect.y += self.vy
        self.collide_y(level)

    def collide_x(self, level):
        for y in range(len(level)):
            for x in range(len(level[0])):
                if level[y][x] in [1, 2, 3, 4]:
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        if self.vx > 0:
                            self.rect.right = tile_rect.left
                            self.vx = -self.vx
                        elif self.vx < 0:
                            self.rect.left = tile_rect.right
                            self.vx = -self.vx

    def collide_y(self, level):
        self.on_ground = False
        for y in range(len(level)):
            for x in range(len(level[0])):
                if level[y][x] in [1, 2, 3, 4]:
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        if self.vy > 0:
                            self.rect.bottom = tile_rect.top
                            self.vy = 0
                            self.on_ground = True
                        elif self.vy < 0:
                            self.rect.top = tile_rect.bottom
                            self.vy = 0

    def draw(self, screen, camera_x):
        """
        if 'GOOMBA_SPRITE' in globals():
            screen.blit(GOOMBA_SPRITE, (self.rect.x - camera_x, self.rect.y))
        else:
        """
        pygame.draw.rect(screen, (139, 69, 19), (self.rect.x - camera_x, self.rect.y, 16 * SCALE, 16 * SCALE))

# Coin class
class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 16 * SCALE, 16 * SCALE)
        self.frame = 0  # For animation

    def update(self):
        self.frame = (self.frame + 1) % 60  # Simple animation cycle

    def draw(self, screen, camera_x):
        """
        if 'COIN_SPRITE' in globals():
            screen.blit(COIN_SPRITE, (self.rect.x - camera_x, self.rect.y))
        else:
        """
        pygame.draw.rect(screen, COIN_YELLOW, (self.rect.x - camera_x, self.rect.y, 16 * SCALE, 16 * SCALE))

# Main game loop
def main():
    clock = pygame.time.Clock()
    mario = Mario(50 * SCALE, 200 * SCALE)
    goombas = [Goomba(200 * SCALE, 200 * SCALE), Goomba(300 * SCALE, 200 * SCALE)]
    coins = [Coin(13 * TILE_SIZE, 4 * TILE_SIZE)]
    camera_x = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        keys = pygame.key.get_pressed()
        mario.update(keys, LEVEL, coins, goombas)
        for goomba in goombas:
            goomba.update(LEVEL)
        for coin in coins:
            coin.update()

        # Camera scrolling
        camera_x = max(0, min(mario.rect.x - SCREEN_WIDTH // 2 + MARIO_WIDTH // 2, len(LEVEL[0]) * TILE_SIZE - SCREEN_WIDTH))

        # Draw
        screen.fill(SKY_BLUE)
        for y in range(len(LEVEL)):
            for x in range(len(LEVEL[0])):
                tile_x = x * TILE_SIZE - camera_x
                if tile_x < -TILE_SIZE or tile_x > SCREEN_WIDTH:
                    continue
                if LEVEL[y][x] == 1:
                    """
                    if 'GROUND_TILE' in globals():
                        screen.blit(GROUND_TILE, (tile_x, y * TILE_SIZE))
                    else:
                    """
                    pygame.draw.rect(screen, GROUND_BROWN, (tile_x, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif LEVEL[y][x] == 2:
                    """
                    if 'BRICK_TILE' in globals():
                        screen.blit(BRICK_TILE, (tile_x, y * TILE_SIZE))
                    else:
                    """
                    pygame.draw.rect(screen, BLOCK_GRAY, (tile_x, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif LEVEL[y][x] == 3:
                    """
                    if 'QBLOCK_TILE' in globals():
                        screen.blit(QBLOCK_TILE, (tile_x, y * TILE_SIZE))
                    else:
                    """
                    pygame.draw.rect(screen, (255, 255, 0), (tile_x, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif LEVEL[y][x] == 4:
                    """
                    if 'PIPE_TILE' in globals():
                        screen.blit(PIPE_TILE, (tile_x, y * TILE_SIZE))
                    else:
                    """
                    pygame.draw.rect(screen, (0, 128, 0), (tile_x, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        mario.draw(screen, camera_x)
        for goomba in goombas:
            goomba.draw(screen, camera_x)
        for coin in coins:
            coin.draw(screen, camera_x)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
