from importlib.machinery import PathFinder
import pygame
import random
import time
from sprites import *
from tkinter import messagebox

runGame = True;
destinationReached = False
steps = 1

white = (255,255,255)

pygame.init()
pathFinderGroup = pygame.sprite.Group()
wallGroup = pygame.sprite.Group()

screen = pygame.display.set_mode((1440, 810))
pygame.display.set_caption("Pathfinder")
screen.fill(white)

def CreateWalls():
    yCoordinate = 50
    for e in range(0, 14):
        i = random.randint(1,3)
        if i == 1:
            rightWall = RightWallObject()
            rightWall.rect.x = 0
            rightWall.rect.y = yCoordinate
            wallGroup.add(rightWall)

        if i == 2:
            leftWall = LeftWallObject()
            leftWall.rect.x = 140
            leftWall.rect.y = yCoordinate
            wallGroup.add(leftWall)
        
        if i == 3:
            middleWall = MiddleWallObject()
            middleWall.rect.x = 70
            middleWall.rect.y = yCoordinate
            wallGroup.add(middleWall)

        yCoordinate+=50

    return wallGroup

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

for wall in walls:
        pathFinder.mask = pygame.mask.from_threshold(pathFinder.image, (0,0,0)) 

def checkCollision():
    if pygame.sprite.spritecollideany(pathFinder, wallGroup, pygame.sprite.collide_mask):
                screen.fill((255, 255, 255))

totalFrames = 0

while runGame: 
    totalFrames+=1
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

    if destinationReached == True:
        runGame = False    

    pathFinder.update()
    pathFinderGroup.draw(screen)
    wallGroup.draw(screen)
    pygame.display.flip()


pygame.quit()
