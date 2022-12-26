from importlib.machinery import PathFinder
import pygame
import random
import time
from sprites import *
from tkinter import messagebox

runGame = True;
steps = 1

white = (255,255,255)
black = (0,0,0)

pygame.init()
pathFinderGroup = pygame.sprite.Group()
wall_list = []

screen = pygame.display.set_mode((1440, 810))
pygame.display.set_caption("Pathfinder")
screen.fill(white)

def CreateWalls():
    yCoordinate = 50

    for e in range(0, 14):
        i = random.randint(1,3)
        if i == 1:
            rightWall = RightWallObject(yCoordinate)
            wall_list.append(rightWall)

        if i == 2:
            leftWall = LeftWallObject(yCoordinate)
            wall_list.append(leftWall)
        
        if i == 3:
            middleWall = MiddleWallObject(yCoordinate)
            wall_list.append(middleWall)

        yCoordinate+=50

    return wall_list

walls = CreateWalls()

pathFinder = PathFinder()
pathFinder.rect.x = 720
pathFinder.rect.y = 765
pathFinderGroup.add(pathFinder)

finishLine = FinishLine()
finishLine.rect.x = 0
finishLine.rect.y = 25
pathFinderGroup.add(finishLine)

mouse = pygame.mouse.get_pos()
keys = pygame.key.get_pressed()
     
while runGame: 

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    pathFinder.control(-steps, 0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    pathFinder.control(steps, 0)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    pathFinder.control(0, -steps)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    pathFinder.control(0, steps)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    pathFinder.control(steps, 0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    pathFinder.control(-steps, 0)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    pathFinder.control(0, steps)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    pathFinder.control(0, -steps)

    for wall in walls:
        wall.draw(screen)





    pathFinder.update()
    pathFinderGroup.draw(screen)
    pygame.display.flip()

pygame.quit()
