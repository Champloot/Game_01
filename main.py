import pygame
from constants_imports import *
from classes import *

pygame.init()
pygame.mixer.init()


def draw_status_bar(hp, dmg, speed, kills=0):
    pygame.draw.rect(screen, ORANGE, (0, 0, 160, 40))
    lst = [hp, dmg, speed, kills]
    for i in range(len(lst)):
        screen.blit(pygame.font.Font(None, 40).render(str(lst[i]), True, WHITE), (i * 40, i))


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            running = False
    if len(Enemies) == 0:
        spawn_creatures()
    screen.fill((0, 0, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    draw_status_bar(Player.life_points, Player.damage, Player.speed, Player.kills)
    pygame.display.flip()
    # all_walls_sprites.update()
    # all_walls_sprites.draw(screen)
