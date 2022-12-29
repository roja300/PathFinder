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

class PathFinderCells(pygame.sprite.Sprite):
    def __init__(self, color):
        super(GridCell, self).__init__()
        self.image = pygame.Surface((19, 19))
        self.color = color

        self.image.fill((self.color))
  
        self.rect = self.image.get_rect()
            
#check if wallCell is there and identify neighrbours
    #for i in wallCells: check rect of wall cells if!= add new cell else return

#work out heuristic and distance
    #end.rect.x - start.rect.x = numx
    #end.rect.y - start.rect.y = numy
    #numx*numx + numy*numy = root(ans)
    #=distance
    
    #start.rect.x - growth.rect.x= numx
    #start.rect.y - growth.rect.y = numy
    #numx*numx + numy*numy = root(ans)
    #=heurestic

    #distance + heurestic = f
    # add f value to each square using 3d aray (x, y, f)

#go and evaluate the neighbour with the lowest f
#move() to that square
