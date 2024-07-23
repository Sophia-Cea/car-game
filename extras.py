from utils import *


class CarPart:
    def __init__(self, dimensions, pos, color=None, screws=[], imageName=None) -> None:
        # screw holes should be drawn onto the img not the screen
        self.dimensions = dimensions
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dimensions[0], self.dimensions[1])
        if imageName == None:
            self.image = pygame.Surface(dimensions)
            if color != None:
                self.image.fill(color)
            else:
                self.image.fill((255,100,100))
        else:
            self.image = pygame.image.load(imageName)
        self.dragging = False
        self.mouseOffset = [0,0]
        self.screwHoles = []
        # rect is in terms of the screen position
        for screw in screws:
            self.screwHoles.append(pygame.Rect(screw[0]+self.rect.x, screw[1]+ self.rect.y, 5,5))
        self.screws = []
        for screw in screws:
            self.screws.append(Screw([screw[0]+self.rect.x, screw[1] + self.rect.y]))
        self.loose = None

    def render(self, screen):
        for hole in self.screwHoles:
            pygame.draw.rect(self.image, (0,0,0), pygame.Rect(hole.x-self.rect.x, hole.y-self.rect.y, hole.w, hole.h))
        screen.blit(self.image, (self.rect.x, self.rect.y))
        for screw in self.screws:
            screw.render(screen)

    def setOffset(self):
        mouse = pygame.mouse.get_pos()
        self.mouseOffset = [mouse[0]-self.rect.x, mouse[1]-self.rect.y]

    def update(self):
        mouse = pygame.mouse.get_pos()
        if self.dragging and self.loose:
            self.rect.x = mouse[0] - self.mouseOffset[0]
            self.rect.y = mouse[1] - self.mouseOffset[1]
        if len(self.screws) == 0:
            self.loose = True
        else:
            self.loose = False

        for screw in self.screws:
            screw.update()


    def handleInput(self, events):
        for event in events:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.loose: 
                    for screw in self.screws:
                        if screw.rect.collidepoint(mouse):
                            screw.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
        for screw in self.screws:
            screw.handleInput(events)



class Screw:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 5,5)
        self.dragging = False

    def render(self, screen):
        pygame.draw.rect(screen, (50,50,50), self.rect)
    
    def update(self):
        if self.dragging:
            mouse = pygame.mouse.get_pos()
            self.rect.x = mouse[0]
            self.rect.y = mouse[1]
    
    def handleInput(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False