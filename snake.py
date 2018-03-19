# imports
import pygame
import random
import bot_player
from pygame.locals import *

# global vars
display_width = 640
display_height = 640
fps = 10
block_size = 10
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (160,214,180)

# initialise pygame
pygame.init()

# clock used for frames per second
clock = pygame.time.Clock()
tick_count = clock.get_time()

font = pygame.font.SysFont('Arial', 20)

# creating surface to execute game on
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake Time!")


# for any alerts to the player
def message_to_screen(text, colour, y_displace = 0):

    text_surface = font.render(text, True, colour)
    text_box = text_surface.get_rect()
    text_box.center = (display_width / 2, display_height / 2 - y_displace)

    game_display.blit(text_surface, text_box)


# draws a block 10x10 (block_size)
def draw_segment(colour, x, y, size_of_block):

    pygame.draw.rect(game_display, colour, [x, y, size_of_block, size_of_block])


# draws the snake
def draw_snake(size_of_block, snake_list):
    for segmentPos in snake_list:
        draw_segment(green, segmentPos[0], segmentPos[1], size_of_block)


# the main game loop (recursive)
def game_loop():
    score = 0
    head_x = display_width / 2
    head_y = display_height / 2
    head_x_change = 0
    head_y_change = 0
    game_exit = False
    game_over = False
    snake_list = []
    snake_length = 5
    human_player = False

    # initial spawning of the apple
    apple_x, apple_y = spawn_apple()

    # difference between game_exit and game_over:
    # game_exit means quit and game_over gives player choice of quit or replay
    while not game_exit:

        # game over handling
        while game_over:
            handle_game_over(score)

            # handling for player clicking cross in top corner
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_over = False
                    game_exit = True
                elif event.type == KEYDOWN and human_player:
                    if event.key == K_q:
                        game_exit = True
                        game_over = False
                    elif event.key == K_SPACE and human_player:
                        game_loop()
                    elif not human_player:
                        game_exit = True
                        game_over = False

        for event in pygame.event.get():
            if event.type == QUIT:
                game_exit = True
            elif event.type == KEYDOWN and human_player:
                head_x_change, head_y_change = process_key_control(event, head_x_change, head_y_change)
            elif not human_player:
                event.key = bot_player.random_direction_bot(tick_count)
                head_x_change, head_y_change = process_key_control(event, head_x_change, head_y_change)

        snake_head = [head_x, head_y]

        game_over = snake_has_crashed(head_x_change, snake_list, snake_head, game_over, head_x, head_y)

        head_x += head_x_change
        head_y += head_y_change

        game_display.fill(black)

        draw_segment(red, apple_x, apple_y, block_size)

        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        draw_snake(block_size, snake_list)

        pygame.display.update()

        if head_x == apple_x and head_y == apple_y:
            apple_x, apple_y, score, snake_length = handle_scoring(apple_x, apple_y, score, snake_length)

        clock.tick(fps)

    pygame.quit()
    quit()


def spawn_apple():
    apple_x = random.randrange(0, (display_width - block_size) / 10) * 10
    apple_y = random.randrange(0, (display_width - block_size) / 10) * 10
    return apple_x, apple_y


def handle_scoring(apple_x, apple_y, score, snake_length):
    apple_x, apple_y = spawn_apple()
    snake_length += 1
    score += 1
    return apple_x, apple_y, score, snake_length


def handle_game_over(score):
    message_to_screen("Game Over...", red, 0)
    message_to_screen("Press SPACE to play again or Q to quit.", red, -20)
    message_to_screen("Score:  " + str(score), green, 20)
    pygame.display.update()


def process_key_control(event, head_x_change, head_y_change):
    if event.key == K_UP and head_y_change <= 0:
        head_y_change = -block_size
        head_x_change = 0
    elif event.key == K_DOWN and head_y_change >=0:
        head_y_change = block_size
        head_x_change = 0
    elif event.key == K_RIGHT and head_x_change >= 0:
        head_y_change = 0
        head_x_change = block_size
    elif event.key == K_LEFT and head_x_change <= 0:
        head_y_change = 0
        head_x_change = -block_size
    return head_x_change, head_y_change


def snake_has_crashed(head_x_change, snake_list, snake_head, game_over, head_x, head_y):
    if head_x_change >= 1:
        for e in snake_list:
            if snake_head == e:
                game_over = True

    if head_x >= display_width or head_y >= display_height or head_x <= 0 or head_y <= 0:
        game_over = True

    return game_over


game_loop()
