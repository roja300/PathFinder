import pygame
from pygame.locals import *
 
# Initiate pygame and give permission
# to use pygame's functionality
pygame.init()
 
# Create a display surface object
# of specific dimension
window = pygame.display.set_mode((600, 600))
 
# Creating a new clock object to
# track the amount of time
clock = pygame.time.Clock()
 
 
# Creating a new rect for first object
player_rect = Rect(200, 500, 50, 50)
 
# Creating a new rect for second object
player_rect2 = Rect(200, 0, 50, 50)
 

gravity = 4
 

run = True
 

while run:
 

    clock.tick(60)
 

    player_rect2.bottom += gravity
 

    collide = pygame.Rect.colliderect(player_rect, p
                                      layer_rect2)
    if collide:
        player_rect2.bottom = player_rect.top
 
    pygame.draw.rect(window, (0,   255,   0),
                     player_rect)
    pygame.draw.rect(window, (0,   0,   255),
                     player_rect2)
 
    pygame.display.update()

    window.fill((255, 255, 255))