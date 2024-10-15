import pygame
import random
import math

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BROWN = (139, 69, 19)
BROWN2 = (87, 52, 16)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (210, 105, 30)
PURPLE = (79, 0, 112)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (124, 252, 0)
AQUA = (11, 156, 129)

# Параметры экрана
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('New_game')

# Создаём группу всех спрайтов, чтобы каждый кадр, каждый спрайт, делал что-то согласно своему классу
all_sprites = pygame.sprite.Group()
all_walls_sprites = pygame.sprite.Group()

# Отслеживание времени, для дальнейшей работы с ним
clock = pygame.time.Clock()
# Ну тут всё ясно, это - фпс(кадры в секунду)
FPS = 60

player_x = 0
player_y = 0
