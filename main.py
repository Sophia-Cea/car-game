import pygame
import sys
from utils import *
from state import *


pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
display = pygame.Surface((WIDTH, HEIGHT))

# stateManager.push(GarageState())
stateManager.push(RepairStateTopView("coronet"))
# stateManager.push(TownState("coronet"))
# stateManager.push(DriveState("coronet"))

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    WIDTH, HEIGHT = screen.get_size()
    stateManager.run(display, events)
    screen.blit(pygame.transform.scale(display, (screen.get_width(), screen.get_height())), (0,0))
    pygame.display.flip()
    
    
    delta = fpsClock.tick(60)/1000