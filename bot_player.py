import random
from pygame.locals import *


def random_direction():
    direction_pointer = random.randrange(0, 3)
    if direction_pointer == 0:
        return K_UP
    elif direction_pointer == 1:
        return K_DOWN
    elif direction_pointer == 2:
        return K_LEFT
    elif direction_pointer == 3:
        return K_RIGHT


def random_direction_bot(count):
    if count % 10 == 0:
        return random_direction()
