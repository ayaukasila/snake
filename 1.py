import pygame
import random

# Инициализация
pygame.init()

# ПОДХОД 1 (как в тетрисе) - сначала задаём КОЛИЧЕСТВО клеток
WIDTH_CELLS = 20        # 20 клеток по ширине
HEIGHT_CELLS = 20       # 20 клеток по высоте
CELL_SIZE = 30          # Размер одной клетки в пикселях

# Вычисляем размер окна (как в тетрисе)
SCREEN_WIDTH = WIDTH_CELLS * CELL_SIZE    # 20 * 30 = 600
SCREEN_HEIGHT = HEIGHT_CELLS * CELL_SIZE  # 20 * 30 = 600

# Настройки экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (70, 70, 70)

# Начальные позиции (используем WIDTH_CELLS и HEIGHT_CELLS)
snake = [(WIDTH_CELLS // 2, HEIGHT_CELLS // 2)]  # Центр: (10, 10)
direction = (1, 0)  # вправо
next_direction = (1, 0)

# Генерация еды
def generate_food():
    while True:
        new_food = (random.randint(0, WIDTH_CELLS - 1), 
                   random.randint(0, HEIGHT_CELLS - 1))
        if new_food not in snake:
            return new_food

food = generate_food()

# Переменные состояния
score = 0
game_over = False

# Таймер движения
MOVE_DELAY = 200  # 200 миллисекунд
last_move_time = 0

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y), 1)

def draw_snake():
    for x, y in snake:
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
        pygame.draw.rect(screen, GREEN, rect)

def draw_food():
    rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
    pygame.draw.rect(screen, RED, rect)

def check_collision():
    head = snake[0]
    
    # Столкновение с границами (используем WIDTH_CELLS и HEIGHT_CELLS)
    if head[0] < 0 or head[0] >= WIDTH_CELLS or head[1] < 0 or head[1] >= HEIGHT_CELLS:
        return True
    
    # Столкновение с собой
    if head in snake[1:]:
        return True
    
    return False

def move_snake():
    global food, score, last_move_time
    
    dx, dy = direction
    head = snake[0]
    new_head = (head[0] + dx, head[1] + dy)
    
    snake.insert(0, new_head)
    
    if new_head == food:
        score += 1
        food = generate_food()
    else:
        snake.pop()
    
    last_move_time = pygame.time.get_ticks()

def reset_game():
    global snake, direction, next_direction, food, score, game_over, last_move_time
    
    snake = [(WIDTH_CELLS // 2, HEIGHT_CELLS // 2)]
    direction = (1, 0)
    next_direction = (1, 0)
    food = generate_food()
    score = 0
    game_over = False
    last_move_time = pygame.time.get_ticks()

# Главный цикл
running = True
last_move_time = pygame.time.get_ticks()

while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                reset_game()
            
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)
    
    if not game_over:
        if next_direction:
            direction = next_direction
        
        if current_time - last_move_time >= MOVE_DELAY:
            move_snake()
            
            if check_collision():
                game_over = True
    
    # Отрисовка
    screen.fill(BLACK)
    draw_grid()
    draw_snake()
    draw_food()
    
    if game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(RED)
        screen.blit(overlay, (0, 0))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()