from pickle import FALSE
from re import A
from tkinter.tix import CELL
from venv import create
import pygame
from classes import *

runGame = True
wallAndBoundsCellsBool = False
finishCellTouched = False
wallCellsBool = False
gridXCoordinates = []
gridYCoordinates = []
#colors
white = (255,255,255)
black = (0,0,0)
green = (0, 153, 76)
pink = (153, 153, 255)
lightPink = (248, 200, 220)
grey = (211, 211, 211)

cellSpace = 20

pygame.init()

#initialize window
screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption("Pathfinder")
screen.fill(white)

#create specific groups
bgCells = pygame.sprite.Group()
wallCells = pygame.sprite.Group()
finishCell = pygame.sprite.Group()
pathFinderCells = pygame.sprite.Group() 
growthCells = pygame.sprite.Group()
outwardGrowthCells = pygame.sprite.Group()

#add all x and y axis coordinates to arrays
def CreateGridCoordinates():
    x = 0
    for i in range(0, 24):
        gridXCoordinates.append(x)
        gridYCoordinates.append(x)
        x+=20;

CreateGridCoordinates()

#get grid coordinates and create black wall
def GetGridCoordinatesIndexAndCreateWall():
    #get mouse location
    mousex, mousey = pygame.mouse.get_pos()
    for y in range(0, 24):
        for x in range(0, 24):
            #check each square for mouse location
            if mousex >= gridXCoordinates[x] and mousex <= (gridXCoordinates[x] + gridXCoordinates[1]) and mousey >= gridYCoordinates[y] and mousey <= (gridYCoordinates[y] + gridYCoordinates[1]):
                #create wall cell and paint it black
                wallCell = GridCell(black)
                wallCell.rect.x = gridXCoordinates[x]
                wallCell.rect.y = gridXCoordinates[y]
                wallCells.add(wallCell)

    global wallCellsBool
    wallCellsBool = True

#create backdrop grid
def CreateCells():
    cellX = 0
    cellY = 0
    for i in range(0, 24):
        for e in range(0, 24):
            cell = GridCell(grey)
            cell.rect.x = cellX
            cell.rect.y = cellY
            bgCells.add(cell)
            cellX+=20
        cellY+=20
        cellX = 0
        
    return bgCells

pathFinderCellX = 0
pathFinderCellY = 0

#create start cell
startCell = GridCell(pink)
startCell.rect.x = pathFinderCellX
startCell.rect.y = pathFinderCellY
pathFinderCells.add(startCell)

#create end cell
endCell = GridCell(green)
endCell.rect.x = gridXCoordinates[23]
endCell.rect.y = gridYCoordinates[23]
finishCell.add(endCell)

#create path finder cell
def CreatePathFinderCell(x, y):
    global pathFinderCellX, pathFinderCellY
    pathFinderCell = GridCell(pink)
    pathFinderCellX+=x
    pathFinderCellY+=y
    pathFinderCell.rect.x = pathFinderCellX
    pathFinderCell.rect.y = pathFinderCellY
    pathFinderCells.add(pathFinderCell)

#decide where pathfinder should be created
def MovePathFinder(direction):
    if direction == "up":
        print("up")
        CreatePathFinderCell(0, -cellSpace)
    elif direction == "down":
        print("down")
        CreatePathFinderCell(0, cellSpace)
    elif direction == "left":
        print("left")
        CreatePathFinderCell(-cellSpace, 0)
    elif direction == "right":
        print("right")
        CreatePathFinderCell(cellSpace, 0)

#save distance and cost of movement

growthCellX = 0
growthCellY = 0

boolCellGrowth = False

def CheckFinish(x, y):
    for finishcell in finishCell:
        if finishcell.rect.x != x and finishcell.rect.y != y:
            boolCellGrowth = False
            return False
#create array instead        

def CheckWalls(x, y):
    print("CheckWallAndBounds called")
    if wallCellsBool == True:
        for wallcell in wallCells:
            if wallcell.rect.x != x and wallcell.rect.y != y:
                return True
            else:
                return False
        else:
            return True

#unsure whether this is necessairy
def IsAlreadyCell(x, y):
    print("DontReplace called")
    for growthcell in growthCells:
        if growthcell.rect.x != x and growthcell.rect.y != y:
            print("return true")
            return False
        else:
            print("return false")
            return True

#create growth cells
def CreateNewGrowthCell(x, y): 
    if CheckWalls(x, y) != True:
        if IsAlreadyCell(x, y) != True:
            growthCell = GridCell(lightPink)
            growthCell.rect.x = x
            growthCell.rect.y = y
            growthCells.add(growthCell)
            outwardGrowthCells.add(growthCell)

        #add to most outward group
        #it seems that cells are being create on top of eachother and that is why it's taking so long
        #remove all from most outward group

        #calculate distance from growth to finish
        #calculate distance from start to growth
    
complete = True

def CellGrowthByOne():
    global complete
    for e in outwardGrowthCells:
        #from each cell create 8 surrounding cells
        growthSpaceX = e.rect.x
        growthSpaceY = e.rect.y
        CreateNewGrowthCell(growthSpaceX, (growthSpaceY - 20))
        CreateNewGrowthCell((growthSpaceX - 20), (growthSpaceY - 20))
        CreateNewGrowthCell((growthSpaceX - 20), growthSpaceY)
        CreateNewGrowthCell((growthSpaceX - 20), (growthSpaceY + 20))
        CreateNewGrowthCell(growthSpaceX, (growthSpaceY + 20))
        CreateNewGrowthCell((growthSpaceX + 20), (growthSpaceY + 20))
        CreateNewGrowthCell((growthSpaceX + 20), growthSpaceY)
        CreateNewGrowthCell((growthSpaceX + 20), (growthSpaceY - 20))

        print("GRID HAD BEEN GROWN")

def GrowthFlow():
    CellGrowthByOne()
    #try to remove all cells and add the most outward ones

#run game
while runGame: 
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                GetGridCoordinatesIndexAndCreateWall()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("SPACE")
                    CreateNewGrowthCell(20, 20)
                    GrowthFlow()
    
    #create backdrop
    grid = CreateCells()

    #draw all elements
    bgCells.draw(screen)
    wallCells.draw(screen)
    finishCell.draw(screen)
    growthCells.draw(screen)
    pathFinderCells.draw(screen)

    pygame.display.flip()

