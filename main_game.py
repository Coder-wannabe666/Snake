import pygame
import random
import time

pygame.init()

def display_score():
    score_surf = font.render(f'SCORE: {score}', False,("white"))
    score_rect = score_surf.get_rect(center=(50, 50))
    screen.blit(score_surf, score_rect)

SCREEN_SIZE = (900, 600)
TILE_SIZE = 50
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 25)
score = 0


running = True
pygame.display.set_caption("Snake")

apple_img = pygame.image.load("apple2.png").convert_alpha()
APPLE_IMAGE_SIZE = (TILE_SIZE, TILE_SIZE)
apple_img = pygame.transform.scale(apple_img, APPLE_IMAGE_SIZE)

cols = SCREEN_SIZE[0] // TILE_SIZE
rows = SCREEN_SIZE[1] // TILE_SIZE

player_col = cols // 2
player_row = rows // 2
player_rect = pygame.Rect(player_col * TILE_SIZE, player_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

apple_col = random.randint(0, cols - 1)
apple_row = random.randint(0, rows - 1)
apple_rect = pygame.Rect(apple_col * TILE_SIZE, apple_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

last_option = 0
last_row = False
last_col = False
move_delay = 0.3
time_since_move = 0

while running:
    dt = clock.tick(60) / 1000
    time_since_move += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_score()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        last_option = -1
        last_row = True
        last_col = False
    if keys[pygame.K_s]:
        last_option = 1
        last_row = True
        last_col = False
    if keys[pygame.K_a]:
        last_option = -1
        last_row = False
        last_col = True
    if keys[pygame.K_d]:
        last_option = 1
        last_row = False
        last_col = True

    if time_since_move >= move_delay:
        time_since_move = 0
        if last_col:
            player_col = max(0, min(cols - 1, player_col + last_option))
        if last_row:
            player_row = max(0, min(rows - 1, player_row + last_option))
        player_rect.topleft = (player_col * TILE_SIZE, player_row * TILE_SIZE)

    screen.fill("black")
    screen.blit(apple_img, apple_rect.topleft)
    pygame.draw.rect(screen, "darkgreen", player_rect)

    for i in range(TILE_SIZE, SCREEN_SIZE[0], TILE_SIZE):
        pygame.draw.line(screen, "red", (i, 0), (i, SCREEN_SIZE[1]))
    for i in range(TILE_SIZE, SCREEN_SIZE[1], TILE_SIZE):
        pygame.draw.line(screen, "red", (0, i), (SCREEN_SIZE[0], i))

    if player_rect.colliderect(apple_rect):
        apple_col = random.randint(0, cols - 1)
        apple_row = random.randint(0, rows - 1)
        apple_rect.topleft = (apple_col * TILE_SIZE, apple_row * TILE_SIZE)
        score += 1



    pygame.display.flip()

pygame.quit()
