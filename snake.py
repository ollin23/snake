from pygame.locals import *
import pygame
import random


# RGB colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# parameters
WIDTH = 600
HEIGHT = 600
FPS = 15
SIZE = 20
grid_x = (WIDTH - SIZE) // SIZE
grid_y = (HEIGHT - SIZE) // SIZE


def initialize():
    pygame.init()
    env = pygame.display.set_mode((WIDTH, HEIGHT))

    snake = [[int(grid_x / 2), int(grid_y / 2)]]
    x_range = (WIDTH - SIZE) // SIZE
    y_range = (HEIGHT- SIZE) // SIZE
    food = [random.randint(0, x_range), random.randint(0, y_range)]

    return env, snake, food


def draw_snake(env, snake, color):
    for x, y in snake:
        pygame.draw.rect(env, color, [x*SIZE, y*SIZE, SIZE, SIZE])


def spawn(env, target, snake, respawn=False):

    if respawn:

        loc = [random.randint(0, grid_x), random.randint(0, grid_y)]
        while loc in snake:
            loc = [random.randint(0, grid_x), random.randint(0, grid_y)]

        return loc
    else:
        # pygame.draw.rect(env, GREEN, [food[0], food[1], SIZE, SIZE])
        pygame.draw.circle(surface=env,
                           color=GREEN,
                           center=[SIZE*target[0]+10, SIZE*target[1]+10],
                           radius=SIZE//2,
                           width=0)


def detect_collision(head, snake, food):
    chit = None
    if head == food:
        print("snek haz et")
        chit = True

    # boundary collisions
    if head[0] > WIDTH-SIZE or head[0] < 0:
        print("out of bounds: x-axis")
        chit = False
    if head[1] > HEIGHT-SIZE or head[1] < 0:
        print("out of bounds: y-axis")
        chit = False

    # self collision
    if len(snake) > 3:
        if head in snake[1:]:
            print("self collision")
            chit = False

    return chit


def move(direction):
    dx, dy = 0, 0
    if direction == 0:
        dy = -SIZE
    if direction == 1:
        dx = -SIZE
    if direction == 2:
        dy = SIZE
    if direction == 3:
        dx = SIZE

    return dx, dy


def display_location(snake):
    x, y = snake[0]
    print(f"length {len(snake)}; location: {x}, {y}")


def display_score(env, score):
    font = pygame.font.SysFont(None, 20)
    text = font.render(f"Score:  {score}", True, WHITE)
    env.blit(text, (5, 5))


def play_game(manual=True):

    # initialize game
    env, snake, food = initialize()
    clock = pygame.time.Clock()
    score = 0
    direction = 3
    dx = SIZE
    dy = 0
    steps = []
    step = 0

    loop = True
    spawn(env, food, snake)
    while loop:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                print("Quit game")
                loop = False
                break

        # manual interface
        if manual:
            pressed = pygame.key.get_pressed()
            if pressed[K_UP] and direction != 2:
                direction = 0
                dx, dy = 0, -SIZE
            if pressed[K_LEFT] and direction != 3:
                direction = 1
                dx, dy = -SIZE, 0
            if pressed[K_DOWN] and direction != 0:
                direction = 2
                dx, dy = 0, SIZE
            if pressed[K_RIGHT] and direction != 1:
                direction = 3
                dx, dy = SIZE, 0
            else:
                pass

        # ai interface
        else:
            pass

        # snake movement
        head = [snake[0][0] + dx, snake[0][1] + dy]
        snake.insert(0, head)
        snake.pop()
        # collision detection
        chit = detect_collision(head, snake, food)
        if chit:
            score += 50
            food = spawn(env, food, snake, True)
            snake.insert(0, head)
            steps.append(step)
            step = 0
        elif chit is None:
            score -= 1
            step += 1
        else:
            loop = False
            break

        # refresh env
        env.fill(BLACK)
        spawn(env, food, snake)
        draw_snake(env, snake, RED)
        clock.tick(FPS)
        display_score(env, score)

    avg_steps = sum(steps) / len(steps)
    return score, avg_steps