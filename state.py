from utils import *
from extras import *

class StateManager:
    def __init__(self) -> None:
        self.queue = []

    def push(self, page):
        self.queue.append(page)
        page.onEnter()

    def pop(self):
        self.queue[len(self.queue)-1].onExit()
        self.queue.pop(len(self.queue)-1)

    def run(self, surface, events):
        self.queue[len(self.queue)-1].update()
        self.queue[len(self.queue)-1].render(surface)
        self.queue[len(self.queue)-1].handleInput(events)

stateManager = StateManager()

class State:
    def __init__(self) -> None:
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def render(self, screen):
        pass

    def update(self):
        pass

    def handleInput(self, events):
        pass


class PlayState(State):
    def __init__(self) -> None:
        super().__init__()

    def render(self, screen):
        super().render(screen)

    def update(self):
        super().update()

    def handleInput(self, events):
        super().handleInput(events)


class GarageState(State):
    def __init__(self) -> None:
        super().__init__()
        self.camera = Camera()
        self.horizontalPos = 0
        self.garageWidth = data.garageSpaces * 220
        self.carRects = []
        for i, car in enumerate(data.car_data):
            self.carRects.append(pygame.Rect(60+i*460, 250, 400,300))
        self.carHovering = -1

    def render(self, screen):
        super().render(screen)
        pygame.draw.rect(screen, (200,200,200), pygame.Rect(0,0, screen.get_width(), screen.get_height()))
        pygame.draw.rect(screen, (100,100,100), pygame.Rect(0,400, screen.get_width(), screen.get_height()))
        for i, car in enumerate(data.car_data):
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.carRects[i].x + self.camera.offset[0], self.carRects[i].y, self.carRects[i].w, self.carRects[i].h))
        if self.carHovering >= 0:
            pygame.draw.rect(screen, (100,0,180), pygame.Rect(200+self.carHovering*460+self.camera.offset[0], 500, 50,50))
            pygame.draw.rect(screen, (80,0,255), pygame.Rect(270+self.carHovering*460+self.camera.offset[0], 500, 50,50))
    
    def update(self):
        super().update()
        self.camera.update()
        mouse = pygame.mouse.get_pos()
        if mouse[0] < 100:
            if self.horizontalPos >= 3:
                self.horizontalPos -= self.horizontalPos/30
        elif mouse[0] > 900:
            if self.horizontalPos <= self.garageWidth - 3:
                self.horizontalPos += (self.garageWidth - self.horizontalPos)/30
        self.camera.lerpToPos([self.horizontalPos + WIDTH/2, 0])
        for i, rect in enumerate(self.carRects):
            if pygame.Rect(rect.x + self.camera.offset[0], rect.y, rect.w, rect.h).collidepoint(mouse):
                self.carHovering = i
                break
            else:
                self.carHovering = -1
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                for i, rect in enumerate(self.carRects):
                    if pygame.Rect(rect.x + self.camera.offset[0], rect.y, rect.w, rect.h).collidepoint(mouse):
                        if pygame.Rect(200+self.carHovering*460+self.camera.offset[0], 500, 50,50).collidepoint(mouse):
                            stateManager.push(DriveState(data.cars[self.carHovering]))
                        elif pygame.Rect(270+self.carHovering*460+self.camera.offset[0], 500, 50,50).collidepoint(mouse):
                            stateManager.push(RepairStateTopView(data.cars[self.carHovering]))
    
    def checkCarDrivable(self, carName):
        # make car slow down when tires are flat
        # make alternator break when belt breaks and become fixed when belt is fixed 
        # battery slowly dies when 
        parts = data.car_data[carName]["parts"]
        if parts["Engine"]["is_broken"]:
            return False
        if parts["Battery"]["is_broken"]:
            return False
        if parts["Fuel Pump"]["is_broken"]:
            return False
        if parts["Spark Plugs"]["is_broken"]:
            return False
        if parts["Carburator"]["is_broken"]:
            return False
        if parts["Transmission"]["is_broken"]:
            return False
        if parts["Alternator"]["is_broken"]:
            return False
        if parts["Starter"]["is_broken"]:
            return False
        if parts["Alternator Belt"]["is_broken"]:
            return False
        if parts["Distributor"]["is_broken"]:
            return False
        if parts["Ignition Coil"]["is_broken"]:
            return False
        
        if data.car_data[carName]["gas"] == "0":
            return False
        return True


class RepairStateTopView(State):
    def __init__(self, carName) -> None:
        super().__init__()
        self.car = carName
        self.changeViewButton = pygame.Rect(20,650, 40,40)
        self.exitButton = pygame.Rect(20,20,60,60)

        self.engine = CarPart([300,350],[350,50],(150,150,150))
        self.carburator = CarPart([100,100], [450,70], (100,100,120))
        self.radiator = CarPart([300,60],[350,540],(100,100,120))
        # self.starter = CarPart([25,40],[],())
        # self.steeringBox = CarPart([20,20],[],())
        self.battery = CarPart([125,100],[180,460],(100,150,100))
        # self.fuelPump = CarPart([15,15],[],())
        # self.alternator = CarPart([20,20],[],())
        self.powerSteeringBelt = CarPart([300,20],[300,430],(200,200,200))
        self.alternatorBelt = CarPart([300,20],[400, 445],(200,200,200))
        # self.distributor = CarPart([25,15],[],())
        # self.ignitionCoil = CarPart([15,15],[],())
        self.leftValveCover = CarPart([50,350],[350,50],(255,0,0))
        self.rightValveCover = CarPart([50,350],[600,50],(255,0,0))
        self.airFilter = CarPart([120,120], [440,60], (200,120,120), [[58,58]])
        # self.coolantTube = 
        # self.sparkPlugWires = 

        # self.sparkPlugs = []
        # for i in range(int(data.car_data[carName]["cylinders"])):
        #     self.sparkPlugs.append(CarPart([10,10], [], (0,255,0)))

        self.renderOrder = [
            self.engine,
            self.leftValveCover,
            self.rightValveCover,
            self.carburator,
            self.airFilter,
            self.battery,
            self.radiator,
            self.powerSteeringBelt,
            self.alternatorBelt
        ]



    def render(self, screen):
        super().render(screen)
        self.drawBackground(screen)
        self.drawCar(screen)
        self.drawButtons(screen)
        self.drawParts(screen)

    def drawBackground(self, screen):
        pygame.draw.rect(screen, (200,200,200), pygame.Rect(0,0, screen.get_width(), screen.get_height()))
        pygame.draw.rect(screen, (100,100,100), pygame.Rect(0,200, screen.get_width(), screen.get_height()))

    def drawCar(self, screen):
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(100,0,800,650))
        pygame.draw.rect(screen, (80,80,80), pygame.Rect(150,0,700,600))

    def drawButtons(self, screen):
        pygame.draw.rect(screen, (80,80,200), self.changeViewButton)
        pygame.draw.rect(screen, (200,80,80), self.exitButton)
    
    def drawParts(self, screen):
        for part in self.renderOrder:
            part.render(screen)


    def update(self):
        super().update()
        for part in self.renderOrder:
                part.update()
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.changeViewButton.collidepoint(mouse):
                    stateManager.pop()
                    stateManager.push(RepairStateSideView(self.car))
                if self.exitButton.collidepoint(mouse):
                    stateManager.pop()
                
                for i in range(len(self.renderOrder)-1, -1, -1):
                    if self.renderOrder[i].rect.collidepoint(mouse):
                        if self.renderOrder[i].loose:
                            self.renderOrder[i].dragging = True
                            self.renderOrder[i].setOffset()
                        break

        for part in self.renderOrder:
            part.handleInput(events)


class RepairStateSideView(State):
    def __init__(self, carName) -> None:
        super().__init__()
        self.car = carName
        self.changeViewButton = pygame.Rect(20,650, 40,40)
        self.exitButton = pygame.Rect(20,20,60,60)

    def render(self, screen):
        super().render(screen)
        pygame.draw.rect(screen, (200,200,200), pygame.Rect(0,0, screen.get_width(), screen.get_height()))
        pygame.draw.rect(screen, (100,100,100), pygame.Rect(0,200, screen.get_width(), screen.get_height()))

        pygame.draw.rect(screen, (255,0,0), pygame.Rect(80,100,840,250))
        pygame.draw.circle(screen, (150,150,150), (190,320), 70)
        pygame.draw.circle(screen, (150,150,150), (750,320), 70)

        pygame.draw.rect(screen, (80,80,200), self.changeViewButton)
        pygame.draw.rect(screen, (200,80,80), self.exitButton)
    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.changeViewButton.collidepoint(mouse):
                    stateManager.pop()
                    stateManager.push(RepairStateTopView(self.car))
                if self.exitButton.collidepoint(mouse):
                    stateManager.pop()


class DriveState(State):
    def __init__(self, carName) -> None:
        super().__init__()
        self.car = carName
        self.tileSize = 80
        with open("road_map.json") as f:
            mapData = json.load(f)
        self.groundMap = mapData["ground map"]
        self.camera = Camera()
        self.carPos = [data.carPos[0] * self.tileSize, data.carPos[0] * self.tileSize]
        self.carTilePos = [12,15]
        self.gas = float(data.car_data[carName]["gas"])
        self.max_gas = float(data.car_data[carName]["max_gas"])
        self.gears = ["p", "d", "r"]
        self.currentGear = "d"
        self.driving = False
        self.velocity = 0
        self.acceleration = float(data.car_data[carName]["acceleration"])
        self.braking = False
        self.brakeSpeed = float(data.car_data[carName]["brake"])
        self.topSpeed = float(data.car_data[carName]["top_speed"])
        self.angle = 0 # facing right

        self.carRect = pygame.Rect(self.carPos[0], self.carPos[1], self.tileSize*.5, self.tileSize*.8)
        self.carImage = pygame.transform.scale(pygame.image.load("car.png"), (self.carRect.w, self.carRect.h))
        self.rotatedCarImage = pygame.transform.rotate(self.carImage, 0)
        
        # place rects
        self.townTileRect = pygame.Rect(34,25,30,17)
        self.townRect = pygame.Rect(self.townTileRect.x*self.tileSize,self.townTileRect.y*self.tileSize, self.townTileRect.w*self.tileSize, self.townTileRect.h*self.tileSize)
        
        self.homeCoords = [8,8]
        self.homeRect = pygame.Rect(self.homeCoords[0]*self.tileSize, self.homeCoords[1]*self.tileSize, self.tileSize,self.tileSize)
        
        self.jobTileRect = pygame.Rect(67,44,11,3)
        self.jobRect = pygame.Rect(self.jobTileRect.x*self.tileSize,self.jobTileRect.y*self.tileSize, self.jobTileRect.w*self.tileSize, self.jobTileRect.h*self.tileSize)
        
        self.gasTileRect = pygame.Rect(9,47, 4,2)
        self.gasRect = pygame.Rect(self.gasTileRect.x*self.tileSize,self.gasTileRect.y*self.tileSize, self.gasTileRect.w*self.tileSize, self.gasTileRect.h*self.tileSize)
        
        # texts
        self.townText = Text("Visit Town", "title", (255,255,255), (50,5), True)
        self.homeText = Text("Go Home", "title", (255,255,255), (50,5), True)
        self.jobText = Text("Go To Work", "title", (255,255,255), (50,5), True)
        self.gasText = Text("Get Gas", "title", (255,255,255), (50,5), True)

    def render(self, screen):
        super().render(screen)
        screen.fill((100, 200, 80))
        self.rotatedCarImage = pygame.transform.rotate(self.carImage, self.angle+90)
        for i in range(len(self.groundMap)):
            for j in range(len(self.groundMap[i])):
                if int(self.groundMap[i][j]) == 0:
                    pygame.draw.rect(screen, (100, 200, 80), pygame.Rect(j*self.tileSize + self.camera.offset[0], i*self.tileSize + self.camera.offset[1], self.tileSize, self.tileSize))
                elif int(self.groundMap[i][j]) == 1:
                    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(j*self.tileSize + self.camera.offset[0], i*self.tileSize + self.camera.offset[1], self.tileSize, self.tileSize))

        screen.blit(self.rotatedCarImage, (self.carPos[0]+self.camera.offset[0], self.carPos[1]+self.camera.offset[1]))

        # draw gas bar
        pygame.draw.rect(screen, (220,220,220), pygame.Rect(30,650,200,20))
        pygame.draw.rect(screen, (120,220,160), pygame.Rect(30,650,200*self.gas/self.max_gas,20))

        # draw rects for various areas
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.townRect.x+self.camera.offset[0],self.townRect.y+self.camera.offset[1], self.townRect.w, self.townRect.h), 4)
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.homeRect.x+self.camera.offset[0],self.homeRect.y+self.camera.offset[1], self.homeRect.w, self.homeRect.h), 4)
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.jobRect.x+self.camera.offset[0],self.jobRect.y+self.camera.offset[1], self.jobRect.w, self.jobRect.h), 4)
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.gasRect.x+self.camera.offset[0],self.gasRect.y+self.camera.offset[1], self.gasRect.w, self.gasRect.h), 4)

        if self.carRect.colliderect(self.townRect):
            self.townText.draw(screen)

        if self.carRect.colliderect(self.homeRect):
            self.homeText.draw(screen)

        if self.carRect.colliderect(self.jobRect):
            self.jobText.draw(screen)

        if self.carRect.colliderect(self.gasRect):
            self.gasText.draw(screen)

    def update(self):
        super().update()
        if self.driving:
            if self.gas > 0:
                if self.velocity <= self.topSpeed/10 - self.acceleration: 
                    self.velocity += self.acceleration
        else:
            if not self.braking:
                if self.velocity >= .07:
                    self.velocity -= .07
                if self.velocity < .07:
                    self.velocity = 0
        if self.braking:
            self.velocity -= self.brakeSpeed
            if self.velocity <= 2:
                self.velocity = 0
        if self.currentGear == "d":
            self.carPos[0] -= self.velocity * math.cos(self.angle * math.pi/180) * delta
            self.carPos[1] += self.velocity * math.sin(self.angle * math.pi/180) * delta
        elif self.currentGear == "r":
            self.carPos[0] += self.velocity * math.cos(self.angle * math.pi/180) * delta
            self.carPos[1] -= self.velocity * math.sin(self.angle * math.pi/180) * delta
        
        if self.velocity != 0:
            self.gas -= self.velocity*.0001

        self.camera.lerpToPos(self.carPos)
        self.camera.update()
        self.angle = self.angle % 360

        self.carRect.x = self.carPos[0]
        self.carRect.y = self.carPos[1]
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    self.driving = True
                if event.key == pygame.K_SPACE:
                    self.braking = True
                if event.key == pygame.K_r:
                    self.currentGear = "r"
                if event.key == pygame.K_d:
                    self.currentGear = "d"
                if event.key == pygame.K_p:
                    self.currentGear = "p"
                
                if event.key == pygame.K_RETURN:
                    if self.carRect.colliderect(self.townRect):
                        stateManager.push(TownState(self.car))

                    if self.carRect.colliderect(self.homeRect):
                        stateManager.pop()

                    if self.carRect.colliderect(self.jobRect):
                        stateManager.push(JobState(self.car))

                    if self.carRect.colliderect(self.gasRect):
                        stateManager.push(GasState(self.car))



            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.driving = False
                if event.key == pygame.K_SPACE:
                    self.braking = False
                

        keys = pygame.key.get_pressed()
        if self.gas > 0:
            if keys[pygame.K_RIGHT]:
                self.angle -= 1
            if keys[pygame.K_LEFT]:
                self.angle += 1


class TownState(State):
    def __init__(self, carName) -> None:
        super().__init__()
        self.car = carName
        self.camera = Camera()
        self.carRect = pygame.Rect(20,400,100,40)
        self.carImg = pygame.Surface((self.carRect.w, self.carRect.h))
        self.carImg.fill((255,0,0))
        self.velocity = 0
        self.acceleration = float(data.car_data[self.car]["acceleration"])
        self.brake = float(data.car_data[self.car]["brake"])
        self.topSpeed = float(data.car_data[self.car]["top_speed"])/10
        self.gas = float(data.car_data[self.car]["gas"])
        self.maxGas = float(data.car_data[self.car]["max_gas"])
        self.driving = False
        self.braking = False
        self.currentGear = "d"

        self.gasStationRect = pygame.Rect(210, 200, 250, 120)
        self.casinoRect = pygame.Rect(490, 100, 300, 220)
        self.bankRect = pygame.Rect(1020, 150, 200, 170)
        self.carStoreRect = pygame.Rect(1300, 200, 200, 120)
        self.restaurantRect = pygame.Rect(1850, 180, 250, 140)
        self.barRect = pygame.Rect(2150, 220, 250, 90)

        # self.boutique1Rect = pygame.Rect()
        # self.boutique2Rect = pygame.Rect()
        # self.boutique3Rect = pygame.Rect()

    def render(self, screen):
        super().render(screen)
        # draw the background
        screen.fill((150,210,255))
        pygame.draw.rect(screen, (0,200,50), pygame.Rect(0,250, WIDTH, 450))
        pygame.draw.rect(screen, (120,120,120), pygame.Rect(0,330, WIDTH, 250))
        
        # draw roads
        pygame.draw.rect(screen, (120,120,120), pygame.Rect(0+self.camera.offset[0],250,200,90))
        pygame.draw.rect(screen, (120,120,120), pygame.Rect(800+self.camera.offset[0],250,200,90))
        pygame.draw.rect(screen, (120,120,120), pygame.Rect(1600+self.camera.offset[0],250,200,90))
        pygame.draw.rect(screen, (120,120,120), pygame.Rect(2400+self.camera.offset[0],250,200,90))
        pygame.draw.rect(screen, (120,120,120), pygame.Rect(3200+self.camera.offset[0],250,200,90))

        # draw buildings
        pygame.draw.rect(screen, (180,180,180), pygame.Rect(self.gasStationRect.x+self.camera.offset[0], self.gasStationRect.y, self.gasStationRect.w, self.gasStationRect.h))
        pygame.draw.rect(screen, (180,180,180), pygame.Rect(self.casinoRect.x+self.camera.offset[0], self.casinoRect.y, self.casinoRect.w, self.casinoRect.h))
        pygame.draw.rect(screen, (180,180,180), pygame.Rect(self.bankRect.x+self.camera.offset[0], self.bankRect.y, self.bankRect.w, self.bankRect.h))
        pygame.draw.rect(screen, (180,180,180), pygame.Rect(self.carStoreRect.x+self.camera.offset[0], self.carStoreRect.y, self.carStoreRect.w, self.carStoreRect.h))
        pygame.draw.rect(screen, (180,180,180), pygame.Rect(self.restaurantRect.x+self.camera.offset[0], self.restaurantRect.y, self.restaurantRect.w, self.restaurantRect.h))
        pygame.draw.rect(screen, (180,180,180), pygame.Rect(self.barRect.x+self.camera.offset[0], self.barRect.y, self.barRect.w, self.barRect.h))

        # pygame.draw.rect(screen, (180,180,180), pygame.Rect(self.boutique1Rect.x+self.camera.offset[0], self.boutique1Rect.y, self.boutique1Rect.w, self.boutique1Rect.h))
        # pygame.draw.rect(screen, (180,180,180), pygame.Rect(self.boutique2Rect.x+self.camera.offset[0], self.boutique2Rect.y, self.boutique2Rect.w, self.boutique2Rect.h))
        # pygame.draw.rect(screen, (180,180,180), pygame.Rect(self.boutique3Rect.x+self.camera.offset[0], self.boutique3Rect.y, self.boutique3Rect.w, self.boutique3Rect.h))
        

        screen.blit(self.carImg, (self.carRect.x+self.camera.offset[0], self.carRect.y+self.camera.offset[1]))
    
    def update(self):
        super().update()
        self.camera.update()
        self.camera.lerpToPos(self.carRect.center)
        if self.driving:
            if self.velocity < self.topSpeed - self.acceleration:
                self.velocity += self.acceleration
        else:
            if self.velocity > .05:
                self.velocity -= .05
            if self.velocity < .03:
                self.velocity = 0

        if self.braking:
            self.velocity *= self.brake
            if self.velocity < .03:
                self.velocity = 0
        
        if self.currentGear == "d":
            self.carRect.x += self.velocity  * delta
        elif self.currentGear == "r":
            self.carRect.x -= self.velocity  * delta
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    self.driving = True
                if event.key == pygame.K_SPACE:
                    self.braking = True
                if event.key == pygame.K_r:
                    self.currentGear = "r"
                if event.key == pygame.K_d:
                    self.currentGear = "d"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.driving = False
                if event.key == pygame.K_SPACE:
                    self.braking = False
            

    

class JobState(State):
    def __init__(self, carName) -> None:
        super().__init__()
        self.car = carName

    def render(self, screen):
        super().render(screen)
    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)


class GasState(State):
    def __init__(self, carName) -> None:
        super().__init__()
        self.car = carName

    def render(self, screen):
        super().render(screen)
    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)