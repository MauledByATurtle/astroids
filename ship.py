import pygame
import math

class Ship:

    def __init__(self, x, y):
        self.pos = [x,y]
        self.velocity = 0
        self.accelerating = True
        self.tri = [0,0,0]
        self.degree = 0
        
        self.ACCELERATION = .02
        self.DEACCELERATION = 0.005
        self.MAXVELOCITY = 2
        self.ROTATESPEED = 1
        self.SIZE = [20,30] #base, height
        self.COLOR = [255,255,255]

        self.BACKPOINTLENGTH = math.sqrt(math.pow((self.pos[0]/2),2) + math.pow((self.pos[1]),2))
        self.BACKLEFTDEGREE = 180 - math.atan((self.pos[0]/2)/(self.pos[1]))
        self.BACKRIGHTDEGREE = 180 + math.atan((self.pos[0]/2)/(self.pos[1]))

    def update(self, surface, keyboard):
        self.updatePhysics(keyboard)
        self.updateShipDraw()
        pygame.draw.polygon(surface, self.COLOR, self.tri, 2)

    def updatePhysics(self, keyboard):
        self.updateRotate(keyboard)
        self.updateAcc(keyboard)
        self.updateVel()
        self.updatePos()

    def updateRotate(self, keyboard):
        if keyboard.getA():
            self.degree += self.ROTATESPEED
        if keyboard.getD():
            self.degree -= self.ROTATESPEED
        

    def updateAcc(self, keyboard):
        if(keyboard.getW()):
            self.accelerating = True
        elif(keyboard.getW() == False):
            self.accelerating = False

    def updateVel(self):
        print(self.velocity)
        if self.accelerating == True:
            self.velocity += self.ACCELERATION
            if self.velocity > self.MAXVELOCITY:
                self.velocity = self.MAXVELOCITY
        if self.accelerating == False and self.velocity > 0:
            self.velocity -= self.DEACCELERATION
            if self.velocity < 0:
                self.velocity = 0

    def updatePos(self):
        self.pos[1] += self.velocity

    def getBackLeftPoint(self):
        return (self.pos[0]+(self.BACKPOINTLENGTH)*math.cos(math.radians(self.degree + self.BACKLEFTDEGREE)),self.pos[1]+(self.BACKPOINTLENGTH)*math.sin(math.radians(self.degree + self.BACKLEFTDEGREE)))

    def getBackRightPoint(self):
        return ((self.pos[0]+(self.SIZE[0]/2)),(self.pos[1]-(self.SIZE[1]/2)))

    def getFrontCenterPoint(self):
        return (self.pos[0]+(self.SIZE[1]/2)*math.cos(math.radians(self.degree)),self.pos[1]+(self.SIZE[1]/2)*math.sin(math.radians(self.degree)))

    def updateShipDraw(self):
        self.tri = (self.getFrontCenterPoint(),self.getBackLeftPoint(),self.getBackRightPoint())
