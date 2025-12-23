import pygame
import random
import sys

# Инициализация pygame
pygame.init()

# -------------------- НАСТРОЙКИ --------------------
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# -------------------- ОКНО --------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)

# -------------------- ФУНКЦИИ --------------------
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN,
                         (segment[0], segment[1], CELL_SIZE, CELL_SIZE))


def draw_food(food):
    pygame.draw.rect(screen, RED,
                     (food[0], food[1], CELL_SIZE, CELL_SIZE))


def show_game_over(score):
    screen.fill(BLACK)
    text1 = font.render("Игра окончена!", True, WHITE)
    text2 = font.render(f"Счёт: {score}", True, WHITE)
    text3 = font.render("Нажмите R для рестарта или Q для выхода", True, WHITE)

    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 130))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 170))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, 210))

    pygame.display.flip()


def random_food():
    x = random.randrange(0, WIDTH, CELL_SIZE)
    y = random.randrange(0, HEIGHT, CELL_SIZE)
    return x, y


# -------------------- ОСНОВНАЯ ИГРА --------------------
def game():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)

    food = random_food()
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)

        # ---------- СОБЫТИЯ ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                        direction = (0, -CELL_SIZE)
                    elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                        direction = (0, CELL_SIZE)
                    elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                        direction = (-CELL_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                        direction = (CELL_SIZE, 0)
                else:
                    if event.key == pygame.K_r:
                        game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        if game_over:
            show_game_over(score)
            continue

        # ---------- ДВИЖЕНИЕ ----------
        head_x = snake[0][0] + direction[0]
        head_y = snake[0][1] + direction[1]
        new_head = (head_x, head_y)

        # ---------- СТОЛКНОВЕНИЯ ----------
        # со стенами
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            game_over = True

        # с собой
        if new_head in snake:
            game_over = True

        snake.insert(0, new_head)

        # ---------- ЕДА ----------
        if new_head == food:
            score += 1
            food = random_food()
        else:
            snake.pop()

        # ---------- ОТРИСОВКА ----------
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)

        score_text = font.render(f"Счёт: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()


# -------------------- ЗАПУСК --------------------
game()
