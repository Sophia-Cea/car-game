import pygame
import json
from utils import *


pygame.init()
HEIGHT, WIDTH = 700, 1000
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([1000, 700], pygame.RESIZABLE)
display = pygame.Surface((1000, 700))
f = open('road_map.json')
data = json.load(f)
f.close()
map = data["ground map"] #2d array
mapWidth = len(map[0])
mapHeight = len(map)
marginX = 65
tileSize = (WIDTH-2*marginX)/mapWidth
marginY = (HEIGHT-mapHeight*tileSize)/2
drawing = False
erasing = False
currentDrawingSetting = 1
coords = Text("(0,0)", "button", (255,255,255), (30, -1), False)


def drawGrid():
    for i in range(mapWidth+1):
        pygame.draw.line(display, (255,255,255), (i*tileSize+marginX, marginY), (i*tileSize+marginX, HEIGHT-marginY), 1)
    for i in range(mapHeight+1):
        pygame.draw.line(display, (255,255,255), (marginX, i*tileSize+marginY), (WIDTH-marginX, i*tileSize+marginY), 1)

def fillGrid():
    for i in range(mapHeight):
        for j in range(mapWidth):
            if map[i][j] == 1:
                pygame.draw.rect(display, (255,255,255), pygame.Rect(j*tileSize+marginX+1, i*tileSize+marginY+1, tileSize, tileSize))
            if map[i][j] == 2:
                pygame.draw.rect(display, (100,100,255), pygame.Rect(j*tileSize+marginX+1, i*tileSize+marginY+1, tileSize, tileSize))
            if map[i][j] == 3:
                pygame.draw.rect(display, (180,180,180), pygame.Rect(j*tileSize+marginX+1, i*tileSize+marginY+1, tileSize, tileSize))
            if map[i][j] == 4:
                pygame.draw.rect(display, (255,210,50), pygame.Rect(j*tileSize+marginX+1, i*tileSize+marginY+1, tileSize, tileSize))
            if map[i][j] == 5:
                pygame.draw.rect(display, (180,0,180), pygame.Rect(j*tileSize + marginX+1, i*tileSize+marginY+1, tileSize, tileSize))



def render():
    display.fill((0,0,0))
    drawGrid()
    fillGrid()
    coords.draw(display)
    if currentDrawingSetting == 1:
        pygame.draw.rect(display, (255,255,255), pygame.Rect(20,20,30,30))
    if currentDrawingSetting == 2:
        pygame.draw.rect(display, (100,100,255), pygame.Rect(20,20,30,30))
    if currentDrawingSetting == 3:
        pygame.draw.rect(display, (180,180,180), pygame.Rect(20,20,30,30))
    if currentDrawingSetting == 4:
        pygame.draw.rect(display, (255,210,50), pygame.Rect(20,20,30,30))
    if currentDrawingSetting == 4:
        pygame.draw.rect(display, (180,0,180), pygame.Rect(20,20,30,30))

def update():
    pos = pygame.mouse.get_pos()
    if pos[0] > marginX and pos[0] < WIDTH-marginX and pos[1] > marginY and pos[1] < HEIGHT-marginY:
        currentTile = (int((pos[0]-marginX)/tileSize), int((pos[1]-marginY)/tileSize))
        coords.reset((255,255,255), str(currentTile))
        if erasing:
            map[currentTile[1]][currentTile[0]] = 0
        if drawing:
            map[currentTile[1]][currentTile[0]] = currentDrawingSetting

def handleInput(events):
    global mapWidth, mapHeight, marginX, marginY, map, tileSize, drawing, erasing, currentDrawingSetting
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                mapHeight += 1
                marginY = (HEIGHT-mapHeight*tileSize)/2
                arr = []
                for _ in range(mapWidth):
                    arr.append(0)
                map.append(arr)
            if event.key == pygame.K_RIGHT:
                mapWidth += 1
                tileSize = (WIDTH-2*marginX)/mapWidth
                marginY = (HEIGHT-mapHeight*tileSize)/2
                for i in range(mapHeight):
                    map[i].append(0)
            if event.key == pygame.K_SPACE:
                erasing = True
            if event.key == pygame.K_1:
                currentDrawingSetting = 1
            if event.key == pygame.K_2:
                currentDrawingSetting = 2
            if event.key == pygame.K_3:
                currentDrawingSetting = 3
            if event.key == pygame.K_4:
                currentDrawingSetting = 4
            if event.key == pygame.K_5:
                currentDrawingSetting = 5

        if event.type == pygame.KEYUP:
            erasing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False




running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            f = open('road_map.json', "w")
            data["ground map"] = map
            json.dump(data, f)
            f.close()
            pygame.quit()

    render()
    handleInput(events)
    update()
    screen.blit(display, (0,0))
    pygame.display.flip()
    delta = fpsClock.tick(60)/1000