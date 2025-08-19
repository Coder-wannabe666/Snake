import pygame
import random
from pathlib import Path
import os

with Path("score.txt").open('r') as file_handle:
    if file_handle.readable() and os.path.getsize("score.txt") != 0:
        highscore = int(file_handle.read())
    else:
        highscore = 0

pygame.init()

SCREEN_SIZE = (900, 600)
TILE_SIZE = 50
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 30)

pygame.display.set_caption("Snake")

apple_img = pygame.image.load("apple2.png").convert_alpha()
APPLE_IMAGE_SIZE = (TILE_SIZE, TILE_SIZE)
apple_img = pygame.transform.scale(apple_img, APPLE_IMAGE_SIZE)

cols = SCREEN_SIZE[0] // TILE_SIZE
rows = SCREEN_SIZE[1] // TILE_SIZE

def display_score():
    score_surf = font.render(f'SCORE: {score}', True, "white")
    score_rect = score_surf.get_rect(midleft=(10, TILE_SIZE // 2))
    screen.blit(score_surf, score_rect)

def display_highscore(highscore):
    highscore_surf = font.render(f'HIGHSCORE: {highscore}', True, "white")
    highscore_rect = highscore_surf.get_rect(midleft=(500, TILE_SIZE // 2))
    screen.blit(highscore_surf, highscore_rect)

def set_new_game():
    global snake, apple_col, apple_row, apple_rect
    global last_option, last_row, last_col, move_delay, time_since_move, first_move
    global score, game_over

    score = 0
    game_over = False

    player_col = cols // 2
    player_row = rows // 2
    snake = [(player_col, player_row)]

    apple_col = random.randint(0, cols - 1)
    apple_row = random.randint(1, rows - 1)
    apple_rect = pygame.Rect(apple_col * TILE_SIZE, apple_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    last_option = 0
    last_row = False
    last_col = False
    move_delay = 0.2
    time_since_move = 0
    first_move = True


set_new_game()

running = True

while running:
    dt = clock.tick(60) / 1000
    time_since_move += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and (not last_row or last_option != 1):
            last_option = -1
            last_row = True
            last_col = False
            first_move = False
        if keys[pygame.K_s] and (not last_row or last_option != -1):
            last_option = 1
            last_row = True
            last_col = False
            first_move = False
        if keys[pygame.K_a] and (not last_col or last_option != 1):
            last_option = -1
            last_row = False
            last_col = True
            first_move = False
        if keys[pygame.K_d] and (not last_col or last_option != -1):
            last_option = 1
            last_row = False
            last_col = True
            first_move = False

        if time_since_move >= move_delay:
            time_since_move = 0
            head_col, head_row = snake[0]

            if last_col:
                head_col += last_option
            if last_row:
                head_row += last_option

            if head_col < 0 or head_col >= cols or head_row < 1 or head_row >= rows:
                game_over = True
                continue

            new_head = (head_col, head_row)

            if new_head in snake and first_move == False:
                game_over = True
                continue

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
        display_highscore(highscore)
        pygame.display.flip()

    else:
        screen.fill("black")
        display_score()
        text_surf = font.render("GAME OVER", True, "red")
        text_rect = text_surf.get_rect(center=(450, 300))
        screen.blit(text_surf, text_rect)
        text_surf = font.render("PRESS R TO RESTART", True, "red")
        text_rect = text_surf.get_rect(center=(450, 400))
        screen.blit(text_surf, text_rect)
        if score > highscore:
            highscore = score
            text_surf = font.render("NEW HIGHSCORE!!!!!!!!!!", True, "red")
            text_rect = text_surf.get_rect(center=(450, 500))
            screen.blit(text_surf, text_rect)
        display_highscore(highscore)
        with Path("score.txt").open('w') as file_handle:
            file_handle.write(str(highscore))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            set_new_game()
            continue

        pygame.display.flip()

pygame.quit()
