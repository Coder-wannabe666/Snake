import pygame
import random
from pathlib import Path
import os

try:
    with Path("score.txt").open('r') as file_handle:
        if os.path.getsize("score.txt") != 0:
            highscore = int(file_handle.read())
        else:
            highscore = 0
except (FileNotFoundError, ValueError):
    highscore = 0

pygame.init()

SCREEN_SIZE = (900, 600)
TILE_SIZE = 50
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 30)

pygame.display.set_caption("Snake")

try:
    apple_img = pygame.image.load("apple2.png").convert_alpha()
    APPLE_IMAGE_SIZE = (TILE_SIZE, TILE_SIZE)
    apple_img = pygame.transform.scale(apple_img, APPLE_IMAGE_SIZE)
except pygame.error:
    apple_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
    apple_img.fill((255, 0, 0))

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
    global snake, apple_arr
    global last_direction, move_delay, time_since_move, time_since_new_apple
    global score, game_over, direction_queue

    score = 0
    game_over = False

    player_col = cols // 2
    player_row = rows // 2
    snake = [(player_col, player_row)]


    apple_arr = []
    for _ in range(1):
        apple_col = random.randint(0, cols - 1)
        apple_row = random.randint(1, rows - 1)
        apple_rect = pygame.Rect(apple_col * TILE_SIZE, apple_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        apple_arr.append(((apple_col, apple_row), apple_rect))

    last_direction = (0, 0)
    direction_queue = []
    move_delay = 0.2
    time_since_move = 0
    time_since_new_apple = 0

set_new_game()

running = True

while running:
    dt = clock.tick(60) / 1000
    time_since_move += dt
    time_since_new_apple += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:

                if event.key == pygame.K_w and last_direction != (0, 1):
                    direction_queue.append((0, -1))
                elif event.key == pygame.K_s and last_direction != (0, -1):
                    direction_queue.append((0, 1))
                elif event.key == pygame.K_a and last_direction != (1, 0):
                    direction_queue.append((-1, 0))
                elif event.key == pygame.K_d and last_direction != (-1, 0):
                    direction_queue.append((1, 0))

    if not game_over:
        if direction_queue:
            last_direction = direction_queue.pop(0)


        if time_since_new_apple >= move_delay * 20:
            time_since_new_apple = 0
            apple_col = random.randint(0, cols - 1)
            apple_row = random.randint(1, rows - 1)
            apple_rect = pygame.Rect(apple_col * TILE_SIZE, apple_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            apple_arr.append(((apple_col, apple_row), apple_rect))

        if time_since_move >= move_delay:
            time_since_move = 0
            head_col, head_row = snake[0]

            head_col += last_direction[0]
            head_row += last_direction[1]


            if head_col < 0 or head_col >= cols or head_row < 1 or head_row >= rows:
                game_over = True
                continue

            new_head = (head_col, head_row)


            if new_head in snake[:-1] and last_direction != (0, 0):
                game_over = True
                continue

            snake.insert(0, new_head)


            apple_eaten = False
            apples_to_remove = []
            for i, (apple_pos, apple_rect) in enumerate(apple_arr):
                if new_head == apple_pos:
                    score += 1
                    apples_to_remove.append(i)
                    apple_eaten = True


            for i in sorted(apples_to_remove, reverse=True):
                apple_arr.pop(i)


            for _ in range(len(apples_to_remove)):
                apple_col = random.randint(0, cols - 1)
                apple_row = random.randint(1, rows - 1)
                apple_rect = pygame.Rect(apple_col * TILE_SIZE, apple_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                apple_arr.append(((apple_col, apple_row), apple_rect))

            if not apple_eaten:
                snake.pop()

        screen.fill("black")
        pygame.draw.rect(screen, "dimgray", (0, 0, SCREEN_SIZE[0], TILE_SIZE))


        for i in range(TILE_SIZE, SCREEN_SIZE[0], TILE_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (i, TILE_SIZE), (i, SCREEN_SIZE[1]))
        for i in range(TILE_SIZE, SCREEN_SIZE[1], TILE_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (0, i), (SCREEN_SIZE[0], i))


        for x_y, apple_rect_ in apple_arr:
            screen.blit(apple_img, apple_rect_)

        for i, (c, r) in enumerate(snake):
            color = "darkgreen" if i > 0 else "green"
            pygame.draw.rect(screen, color, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))

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
            with Path("score.txt").open('w') as file_handle:
                file_handle.write(str(highscore))
        display_highscore(highscore)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            set_new_game()

        pygame.display.flip()

pygame.quit()