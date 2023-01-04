from pdb import Restart
from tkinter import CURRENT
from tkinter.tix import CELL
import pygame
from classes import *
import pandas as pd

runGame = True
isFinished = False
beginGrowth = False
wallAndBoundsCellsBool = False
finishCellTouched = False
wallCellsBool = False
recentNorth = False
recentEast = False
recentSouth = False
recentWest = False
seekFinish = False
replaceGrowth = False
additionalPath = False

#colors
white = (255,255,255)
black = (0,0,0)
green = (0, 153, 76)
pink = (153, 153, 255)
lightPink = (248, 200, 220)
grey = (211, 211, 211)
darkGrey = (120, 120, 120)
darkPurple = (48, 25, 52)

#initalising values
cellSpace = 20
amount = 0
growthCellX = 0
growthCellY = 0
pathFinderCellX = 240
pathFinderCellY = 0
pathX = 0
pathY = 0
cellsMoved = 0
potentialPaths = 0
pathsFound = 0
iterations = 1

#initialising arrays
cellsMovedArray = []
gridXCoordinates = []
gridYCoordinates = []
dynamicCellX = []
dynamicCellY = []
potentialPathPointX = []
potentialPathPointY = []

#initialising pygame
pygame.init()

#initialize window
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Pathfinder")
screen.fill(white)

#create specific groups
bgCells = pygame.sprite.Group()
wallCells = pygame.sprite.Group()
endCells = pygame.sprite.Group()
pathFinderCells = pygame.sprite.Group() 
newestPathFinder = pygame.sprite.GroupSingle() 
growthCells = pygame.sprite.Group()
currentGrowthCells = pygame.sprite.Group()
cellUsed = pygame.sprite.Group()
startCells = pygame.sprite.Group()
collisionCells = pygame.sprite.Group()

#add all x and y axis coordinates to arrays
def CreateGridCoordinates():
    x = 0
    for i in range(0, 25):
        gridXCoordinates.append(x)
        gridYCoordinates.append(x)
        x+=20;

CreateGridCoordinates()

#get grid coordinates and create black wall
def GetGridCoordinatesIndexAndCreateWall():
    #get mouse location
    mousex, mousey = pygame.mouse.get_pos()
    for y in range(0, 25):
        for x in range(0, 25):
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
    for i in range(0, 25):
        for e in range(0, 25):
            cell = GridCell(grey)
            cell.rect.x = cellX
            cell.rect.y = cellY
            bgCells.add(cell)
            cellX+=20
        cellY+=20
        cellX = 0
        
    return bgCells

#create start cell
startCell = GridCell(pink)
startCell.rect.x = pathFinderCellX
startCell.rect.y = pathFinderCellY
startCells.add(startCell)

#create end cell
endCell = GridCell(green)
endCell.rect.x = gridXCoordinates[12]
endCell.rect.y = gridYCoordinates[5]
endCells.add(endCell)

#create cell when there is a collision withing pathfinder
def CreateCollisionCell(x, y):
    collisionCell = GridCell(darkPurple)
    collisionCell.rect.x = x
    collisionCell.rect.y = y
    collisionCells.add(collisionCell)

    for e in growthCells:
        if e.rect.x == x and e.rect.y == y:
            e.kill()

    for e in currentGrowthCells:
        if e.rect.x == x and e.rect.y == y:
            e.kill()

#when there is a collision path is restarted excluding collision cells
def RestartPathWithCollision(x, y):
    global runGame
    global recentNorth, recentEast, recentSouth, recentWest
    for e in growthCells:
        for i in currentGrowthCells:
            if i.rect.x != e.rect.x and i.rect.y != e.rect.y:
                currentGrowthCells.add(e)

    for e in growthCells:
        if recentNorth:
            if e.rect.x == x and e.rect.y == y - cellSpace:
                CreateCollisionCell(x, y - cellSpace)
                print("recent north")
                break
        elif recentEast:
            if e.rect.x == x + cellSpace and e.rect.y == y:
                CreateCollisionCell(x + cellSpace, y)
                print("recent east")
                break
        elif recentSouth:
            if e.rect.x == x and e.rect.y == y + cellSpace:
                CreateCollisionCell(x, y + cellSpace)
                print("recent south")
                break
        elif recentWest:
            if e.rect.x == x - cellSpace and e.rect.y == y:
                CreateCollisionCell(x - cellSpace, y)
                print("recent west")
                break

    #restart pathfinder
    for e in pathFinderCells:
            e.kill()

#create path finder cell
def CreatePathFinderCell(x, y):
    global pathFinderCellX, pathFinderCellY, cellsMoved, replaceGrowth
    pathFinderCell = GridCell(pink)
    pathFinderCellX+=x
    pathFinderCellY+=y
    pathFinderCell.rect.x = pathFinderCellX
    pathFinderCell.rect.y = pathFinderCellY
    pathFinderBackCollision = pygame.sprite.spritecollide(pathFinderCell, pathFinderCells, False)
    if pathFinderBackCollision or pathFinderCellX < 0 or pathFinderCellX > 480 or pathFinderCellY < 0 or pathFinderCellX > 480:
        print("COLLISION")
        pathFinderCell.kill()
        RestartPathWithCollision(pathFinderCellX, pathFinderCellY)
        #if x and y of current growth is not in growth add it back to growth
        pathFinderCellX = 0
        pathFinderCellY = 0
        CreatePathFinderCell(240, 0)
        while replaceGrowth:
            CellGrowthByOne()
    else:
        pathFinderCells.add(pathFinderCell)
        newestPathFinder.add(pathFinderCell)
        cellsMoved = cellsMoved + 1
        print(cellsMoved)

#decide where pathfinder should be created
def MovePathFinder(direction):
    if direction == "north":
        print("north")
        CreatePathFinderCell(0, -cellSpace)
    elif direction == "south":
        print("south")
        CreatePathFinderCell(0, cellSpace)
    elif direction == "west":
        print("west")
        CreatePathFinderCell(-cellSpace, 0)
    elif direction == "east":
        print("east")
        CreatePathFinderCell(cellSpace, 0)

#create growth cells
def CreateNewGrowthCell(x, y):
    global recentNorth, recentEast, recentSouth, recentWest, isFinished, replaceGrowth
    tempCell = GridCell(lightPink)
    tempCell.rect.x = x
    tempCell.rect.y = y
    growthCollision = pygame.sprite.spritecollide(tempCell, growthCells, False)
    wallCollision = pygame.sprite.spritecollide(tempCell, wallCells, False)
    endCollision = pygame.sprite.spritecollide(tempCell, endCells, False)
    blockCollision = pygame.sprite.spritecollide(tempCell, collisionCells, False)
    #if growth cell x and y are not in current growth cell it add it back to growth cell
    if endCollision:
        isFinished = True
    elif growthCollision or wallCollision or x < 0 or y < 0 or x > 480 or y > 480:
        print("COLLISION")
        tempCell.remove()
    elif blockCollision:
        replaceGrowth = False
    else:
        print("CELL ADDED AT", x, y)
        growthCell = GridCell(lightPink)
        growthCell.rect.x = x
        growthCell.rect.y = y
        growthCell.distance = growthCell.CalculateDistance(startCell.rect.x, startCell.rect.y, growthCell.rect.x, growthCell.rect.y, endCell.rect.x, endCell.rect.y)
        print("CELL GIVEN DISTANCE:", growthCell.distance)
        growthCells.add(growthCell)
        currentGrowthCells.add(growthCell)
    return amount

def CellGrowthByOne():
    global complete
    for e in growthCells:
        #from each cell create 4 surrounding cells
        growthSpaceX = e.rect.x
        growthSpaceY = e.rect.y
        CreateNewGrowthCell(growthSpaceX, (growthSpaceY - 20))
        CreateNewGrowthCell((growthSpaceX - 20), growthSpaceY)
        CreateNewGrowthCell(growthSpaceX, (growthSpaceY + 20))
        CreateNewGrowthCell((growthSpaceX + 20), growthSpaceY)

#check whether the program should complete another iteration
def AddionalPathPointAdd():
    global additionalPath, potentialPaths
    if additionalPath:
        for e in newestPathFinder:
            print("Potential second path found...", e.rect.x, e.rect.y)
            potentialPathPointX.append(e.rect.x)
            potentialPathPointY.append(e.rect.y)   
            potentialPaths = potentialPaths + 1

    additionalPath = False
      
def SeekNextCell():
    #set pathX, pathY to rect pathfindercell
    global recentNorth, recentEast, recentSouth, recentWest, potentialPaths, pathX, pathY, pathFinderCellX, pathFinderCellY, additionalPath
    distanceArray = []
    findSmallestDistanceArray = []

    #gather up, down left, right growth cells
    sDistance = 10000000000
    nDistance = 10000000000
    wDistance = 10000000000
    eDistance = 10000000000

    for e in newestPathFinder:
        print(e.rect.x, e.rect.y)
        pathX = e.rect.x
        pathY = e.rect.y

    #save distance of surrounding cells
    for e in currentGrowthCells:
        if e.rect.x == pathX and e.rect.y == pathY + cellSpace:
            sDistance = e.distance
        if e.rect.x == pathX - cellSpace and e.rect.y == pathY:
            wDistance = e.distance
        if e.rect.x == pathX + cellSpace and e.rect.y == pathY:
            eDistance = e.distance
        if e.rect.x == pathX and e.rect.y == pathY - cellSpace:
            nDistance = e.distance

    #find smallest value's index
    distanceArray = [nDistance, sDistance, eDistance, wDistance]
    findSmallestDistanceArray = [nDistance, wDistance, sDistance, eDistance]
    print(distanceArray)
    findSmallestDistanceArray.sort()
    smallestDistanceIndex = (pd.Series(distanceArray).idxmin())

    if findSmallestDistanceArray[0] == findSmallestDistanceArray[1] and pathX > 0 and pathY > 0:
        additionalPath = True

    #horizontal & vertical movement depending on shortest distance
    if smallestDistanceIndex == 0:
        AddionalPathPointAdd()
        MovePathFinder("north")
        recentNorth = True
        recentEast = False 
        recentSouth = False 
        recentWest = False
        pathY=-cellSpace

        for e in growthCells:
            for i in newestPathFinder:
                if e.rect.x == i.rect.x and e.rect.y == i.rect.y:
                    currentGrowthCells.remove(e)
    elif smallestDistanceIndex == 1:
        AddionalPathPointAdd()
        MovePathFinder("south")
        recentNorth = False
        recentEast = False 
        recentSouth = True 
        recentWest = False
        pathY=+cellSpace
        for e in growthCells:
            for i in newestPathFinder:
                if e.rect.x == i.rect.x and e.rect.y == i.rect.y:
                    currentGrowthCells.remove(e)
    elif smallestDistanceIndex == 2:
        AddionalPathPointAdd()
        MovePathFinder("east")
        recentNorth = False
        recentEast = True 
        recentSouth = False 
        recentWest = False
        pathX=+cellSpace
        for e in growthCells:
            for i in newestPathFinder:
                if e.rect.x == i.rect.x and e.rect.y == i.rect.y:
                    currentGrowthCells.remove(e)
    elif smallestDistanceIndex == 3:
        AddionalPathPointAdd()
        MovePathFinder("west")
        recentNorth = False
        recentEast = False 
        recentSouth = False 
        recentWest = True
        pathX=-cellSpace
        for e in growthCells:
            for i in newestPathFinder:
                if e.rect.x == i.rect.x and e.rect.y == i.rect.y:
                    currentGrowthCells.remove(e)

def WipeAndNewIteration():
    for e in pathFinderCells:
        e.kill()
    for e in newestPathFinder:
        e.kill()

    CreatePathFinderCell(240, 0)

counter = 0

def CheckForAdditionalIteration():
    global seekFinish, potentialPaths, pathsFound
    print(potentialPathPointX, potentialPathPointY)
    if all(potentialPathPointX):
        print("ANOTHER ITERATION")
        print("POTENTIAL PATHS:", potentialPaths)
        print("PATHS FOUND:", pathsFound)
        WipeAndNewIteration()
        seekFinish = True

finishedIteration = False

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
                    CreateNewGrowthCell(startCell.rect.x, startCell.rect.y)
                    beginGrowth = True
                if event.key == pygame.K_s:
                    seekFinish = True
    
    #create backdrop
    grid = CreateCells()

    if beginGrowth == True and isFinished != True:
        CellGrowthByOne()
        #cell growth by one

    if seekFinish == True:
        SeekNextCell()
        for e in endCells:
            for i in newestPathFinder:
                if e.rect.x - 20 == i.rect.x and e.rect.y == i.rect.y:
                    print("PATH FOUND")
                    seekFinish = False
                    finishedIteration = True
                if e.rect.x + 20 == i.rect.x and e.rect.y == i.rect.y:
                    print("PATH FOUND")
                    seekFinish = False
                    finishedIteration = True
                if e.rect.x == i.rect.x and e.rect.y == i.rect.y  + 20 :
                    print("PATH FOUND")
                    seekFinish = False
                    finishedIteration = True
                if e.rect.x == i.rect.x and e.rect.y == i.rect.y - 20:
                    print("PATH FOUND")
                    seekFinish = False
                    finishedIteration = True
                    
                
    #draw all elements
    bgCells.draw(screen)
    wallCells.draw(screen)
    growthCells.draw(screen)
    endCells.draw(screen)
    pathFinderCells.draw(screen)
    startCells.draw(screen)
    collisionCells.draw(screen)

    if seekFinish == False and finishedIteration == True:
        CheckForAdditionalIteration()
        cellsMovedArray.append(cellsMoved)
        print(cellsMovedArray)
        finishedIteration = False

    pygame.display.flip()

