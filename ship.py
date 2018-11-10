import pygame
import math

class Ship:

    def __init__(self, x, y):
        self.pos = [x,y]
        self.velocity = 0
        self.accelerating = True
        self.tri = [0,0,0]
        self.degree = 0
        self.deacceleration = 0
        
        self.ACCELERATION = .02
        self.FRICTION = 0.005
        self.MAXVELOCITY = 1
        self.ROTATESPEED = 0.5
        self.SIZE = [20,30] #base, height
        self.COLOR = [255,255,255]

        self.BACKPOINTLENGTH = math.sqrt(math.pow((self.SIZE[0]/2),2) + math.pow((self.SIZE[1]/2),2))
        self.BACKLEFTDEGREE = 180 - math.degrees((math.atan((self.SIZE[0]/2)/(self.SIZE[1]/2))))
        self.BACKRIGHTDEGREE = 180 +  math.degrees((math.atan((self.SIZE[0]/2)/(self.SIZE[1]/2))))

    def update(self, surface, keyboard, clock, size):
        self.updatePhysics(keyboard, clock, size)
        self.updateShipDraw()
        pygame.draw.polygon(surface, self.COLOR, self.tri, 2)
        pygame.draw.line(surface, (255,0,0), self.pos, self.pos, 1)

    def updatePhysics(self, keyboard, clock, size):
        self.updateRotate(keyboard, clock)
        self.updateAcc(keyboard)
        self.updateVel()
        self.updatePos(clock, size)

    def updateRotate(self, keyboard, clock):
        time = clock.tick(60)
        if keyboard.getA():
            self.degree -= self.ROTATESPEED * time
        if keyboard.getD():
            self.degree += self.ROTATESPEED * time
        
    def updateAcc(self, keyboard):
        if(keyboard.getW()):
            self.accelerating = True
        elif(keyboard.getW() == False):
            self.accelerating = False

        if(keyboard.getS()):
            self.deacceleration = self.ACCELERATION
        elif(keyboard.getS() == False):
            self.deacceleration = self.FRICTION
            

    def updateVel(self):
        if self.accelerating == True:
            self.velocity += self.ACCELERATION
            if self.velocity > self.MAXVELOCITY:
                self.velocity = self.MAXVELOCITY
        if self.accelerating == False and self.velocity > 0:
            self.velocity -= self.deacceleration
            if self.velocity < 0:
                self.velocity = 0

    def updatePos(self, clock, size):
        time = clock.tick(60)
        self.pos[0] += (self.velocity * time)*math.cos(math.radians(self.degree))
        self.pos[1] += (self.velocity * time)*math.sin(math.radians(self.degree))
        self.checkAllBounds(size)


    def checkAllBounds(self, size):
        self.checkBoundTop(size[1])
        self.checkBoundBot(size[1])
        self.checkBoundRight(size[0])
        self.checkBoundLeft(size[0])

    def checkBoundTop(self, height):
        if self.pos[1] > height:
            self.pos[1] = 0

    def checkBoundBot(self, height):
        if self.pos[1] < 0:
            self.pos[1] = height

    def checkBoundRight(self, width):
        if self.pos[0] > width:
            self.pos[0] = 0

    def checkBoundLeft(self, width):
        if self.pos[0] < 0:
            self.pos[0] = width

    def getBackLeftPoint(self):
        return (self.pos[0]+(self.BACKPOINTLENGTH)*math.cos(math.radians(self.degree + self.BACKLEFTDEGREE)),self.pos[1]+(self.BACKPOINTLENGTH)*math.sin(math.radians(self.degree + self.BACKLEFTDEGREE)))

    def getBackRightPoint(self):
        return (self.pos[0]+(self.BACKPOINTLENGTH)*math.cos(math.radians(self.degree + self.BACKRIGHTDEGREE)),self.pos[1]+(self.BACKPOINTLENGTH)*math.sin(math.radians(self.degree + self.BACKRIGHTDEGREE)))

    def getFrontCenterPoint(self):
        return (self.pos[0]+(self.SIZE[1]/2)*math.cos(math.radians(self.degree)),self.pos[1]+(self.SIZE[1]/2)*math.sin(math.radians(self.degree)))

    def updateShipDraw(self):
        self.tri = (self.getFrontCenterPoint(),self.getBackLeftPoint(),self.getBackRightPoint())
