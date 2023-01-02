from calendar import c
import math
import pygame

white = (255,255,255)
black = (0,0,0)
green = (0, 153, 76)
pink = (153, 153, 255)
grey = (211, 211, 211)

class GridCell(pygame.sprite.Sprite):
    def __init__(self, color):
        super(GridCell, self).__init__()
        self.image = pygame.Surface((19, 19))
        self.color = color

        self.image.fill((self.color))
  
        self.rect = self.image.get_rect()
        self.distance = 0

    def CalculateDistance(self, startX, startY, currentX, currentY, endX, endY):
        #pythag theoreom without square root because it is unneccessairy
        a = currentX - endX
        b = currentY - endY
        c = startX - currentX
        d = startY - currentY
        cost = complex(math.sqrt((a ** 2 + b ** 2)))
        totalCells = a ** 2 + b ** 2
        travelCost = complex(math.sqrt((c ** 2 + d ** 2)))
        #when value is at a right angle the value thinks it's further away than it is
        cost = cost.real - travelCost.real
        return totalCells
