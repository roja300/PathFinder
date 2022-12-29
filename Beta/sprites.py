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
        
        self.mask = pygame.mask.from_threshold(self.image,(0,0,0),(0,0,0))
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #aesthetics
        self.image = pygame.Surface((1300, 5))
        self.image.fill(('black'))

        self.rect = self.image.get_rect()

class LeftWallObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #aesthetics
        self.image = pygame.Surface((1300, 5))
        self.image.fill(('black'))

        self.rect = self.image.get_rect()
        

class MiddleWallObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #aesthetics
        self.image = pygame.Surface((1300, 5))
        self.image.fill(('black'))

        self.rect = self.image.get_rect()

