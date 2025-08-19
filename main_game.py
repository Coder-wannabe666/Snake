import pygame
import random

pygame.init()

def display_score():
    score_surf = font.render(f'SCORE: {score}', True, "white")
    score_rect = score_surf.get_rect(midleft=(10, TILE_SIZE // 2))
    screen.blit(score_surf, score_rect)

SCREEN_SIZE = (900, 600)
TILE_SIZE = 50
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 30)
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
snake = [(player_col, player_row)]


apple_col = random.randint(0, cols - 1)
apple_row = random.randint(1, rows - 1)  # też nie w pierwszym rzędzie
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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and (last_option != 1 or last_row == False):
        last_option = -1
        last_row = True
        last_col = False
    if keys[pygame.K_s] and (last_option == 1 or last_row == False):
        last_option = 1
        last_row = True
        last_col = False
    if keys[pygame.K_a] and (last_option != 1 or last_col == False):
        last_option = -1
        last_row = False
        last_col = True
    if keys[pygame.K_d] and (last_option == 1 or last_col == False):
        last_option = 1
        last_row = False
        last_col = True

    if time_since_move >= move_delay:
        time_since_move = 0
        head_col, head_row = snake[0]

        if last_col:
            head_col += last_option
            head_col = max(0, min(cols - 1, head_col))
        if last_row:
            head_row += last_option
            head_row = max(0, min(rows - 1, head_row))
        new_head = (head_col, head_row)
        snake.insert(0, new_head)
        if new_head == (apple_col, apple_row):
            score += 1
            apple_col = random.randint(0, cols - 1)
            apple_row = random.randint(1, rows - 1)
            apple_rect.topleft = (apple_col * TILE_SIZE, apple_row * TILE_SIZE)
        else:
            snake.pop()

    screen.fill("black")


    pygame.draw.rect(screen, "dimgray", (0, 0, SCREEN_SIZE[0], TILE_SIZE))


    screen.blit(apple_img, apple_rect.topleft)
    for (c, r) in snake:
        pygame.draw.rect(screen, "darkgreen", (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))


    for i in range(TILE_SIZE, SCREEN_SIZE[0], TILE_SIZE):
        pygame.draw.line(screen, "red", (i, TILE_SIZE), (i, SCREEN_SIZE[1]))
    for i in range(TILE_SIZE, SCREEN_SIZE[1], TILE_SIZE):
        pygame.draw.line(screen, "red", (0, i), (SCREEN_SIZE[0], i))


    display_score()
    pygame.display.flip()

pygame.quit()
