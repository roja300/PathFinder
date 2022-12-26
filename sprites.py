import pygame
import sys

objects = []

class PathFinder(pygame.sprite.Sprite):
    def __init__(self):
        super(PathFinder, self).__init__()
  
        #aesthetics
        self.image = pygame.Surface((10, 10))
        self.image.fill((53, 94, 59))
  
        self.rect = self.image.get_rect()
        
        #movement
        self.movex = 0
        self.movey = 0
        self.frame = 0

    def control(self, x, y):
        self.movex += x
        self.movey += y

    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

class FinishLine(pygame.sprite.Sprite):
    def __init__(self):
        super(FinishLine, self).__init__()
  
        #aesthetics
        self.image = pygame.Surface((1440, 5))
        self.image.fill((175, 225, 175))
  
        self.rect = self.image.get_rect()

class RightWallObject(pygame.sprite.Sprite):
    def __init__(self, y):
        #aesthetics
        self.width = 1300
        self.height = 5
        self.x = 140
        self.y = y

        self.image = pygame.Surface((self.width, self.height))

        self.player_main = pygame.transform.scale(self.image, (1300,5))

        self.isSolid = True

    def draw(self, background):
        background.blit(self.player_main, (self.x, self.y))

class LeftWallObject(pygame.sprite.Sprite):
    def __init__(self, y):
        #aesthetics
        self.width = 1300
        self.height = 5
        self.x = 0
        self.y = y

        self.image = pygame.Surface((self.width, self.height))

        self.player_main = pygame.transform.scale(self.image, (1300,5))

        self.isSolid = True

    def draw(self, background):
        background.blit(self.player_main, (self.x, self.y))
        

class MiddleWallObject(pygame.sprite.Sprite):
    def __init__(self, y):
        #aesthetics
        self.width = 1300
        self.height = 5
        self.x = 70
        self.y = y

        self.image = pygame.Surface((self.width, self.height))

        self.player_main = pygame.transform.scale(self.image, (1300,5))

        self.isSolid = True

    def draw(self, background):
        background.blit(self.player_main, (self.x, self.y))

