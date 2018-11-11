import pygame
import shot_basic
import math

class Ship:

    def __init__(self, x, y):
        self.pos = [x,y]
        self.velocity = [0,0]
        self.accelerating = True
        self.tri = [0,0,0]
        self.degree = 0
        self.deacceleration = 0

        self.bulletsArray = []
        self.bulletShot = False
        
        self.ACCELERATION = .02
        self.FRICTION = 0.005
        self.MAXVELOCITY = 1
        self.ROTATESPEED = 0.5
        self.SIZE = [20,30] #base, height
        self.COLOR = [255,255,255]

        self.BACKPOINTLENGTH = self.pythag(self.SIZE[0]/2, self.SIZE[1]/2)
        self.BACKLEFTDEGREE = 180 - math.degrees((math.atan((self.SIZE[0]/2)/(self.SIZE[1]/2))))
        self.BACKRIGHTDEGREE = 180 +  math.degrees((math.atan((self.SIZE[0]/2)/(self.SIZE[1]/2))))

    def update(self, surface, keyboard, clock, size):
        self.updatePhysics(keyboard, clock, size)
        self.updateShipDraw()
        self.drawShip(surface)

    def drawShip(self, surface):
        pygame.draw.polygon(surface, self.COLOR, self.tri, 2)
        pygame.draw.line(surface, (255,0,0), self.pos, self.pos, 1)

    def updateShots(self, surface, keyboard, clock, size):
        self.checkShooting(keyboard)

        counter = 0
        for shot in self.bulletsArray:
            shot.update(surface, clock)
            if shot.checkAllBounds(size):
                self.bulletsArray.pop(counter)
            counter += 1

    def checkShooting(self,keyboard):
        if keyboard.getSpace() and self.bulletShot == False:
            self.bulletShot = True
            self.bulletsArray.append(shot_basic.ShotBasic(self.pos[0], self.pos[1], self.degree))
        elif keyboard.getSpace() == False and self.bulletShot == True:
            self.bulletShot = False

    def updatePhysics(self, keyboard, clock, size):
        self.updateRotate(keyboard, clock)
        self.updateAcc(keyboard)
        self.updateVel()
        self.updatePos(size,clock)

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
            self.velocity[0] += self.trigX(self.ACCELERATION,self.degree)
            self.velocity[1] += self.trigY(self.ACCELERATION,self.degree)

        self.velocity[0] = self.updateVelocityParamater(self.velocity[0])
        self.velocity[1] = self.updateVelocityParamater(self.velocity[1])
            
    def updateVelocityParamater(self,velocityXorY):
        if velocityXorY < -self.MAXVELOCITY:
            vevelocityXorYl = -self.MAXVELOCITY
            
        if velocityXorY > self.MAXVELOCITY:
            velocityXorY = self.MAXVELOCITY

        if self.accelerating == False and abs(velocityXorY > 0):
            if velocityXorY > 0:
                velocityXorY -= self.deacceleration
                if velocityXorY < 0:
                    velocityXorY = 0
                    
            elif velocityXorY < 0:
                velocityXorY += self.deacceleration
                if velocityXorY > 0:
                    velocityXorY = 0

        return velocityXorY

    def updatePos(self, size, clock):
        time = clock.tick(60)
        self.pos[0] += self.velocity[0]*time
        self.pos[1] += self.velocity[1]*time
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

    def pythag(self,a,b):
        return math.sqrt(math.pow(a,2)+math.pow(b,2))

    def trigX(self,length,deg):
        return length*math.cos(math.radians(deg))

    def trigY(self,length,deg):
        return length*math.sin(math.radians(deg))

    def getBackLeftPoint(self):
        return (self.pos[0]+self.trigX((self.BACKPOINTLENGTH),self.degree + self.BACKLEFTDEGREE)),self.pos[1]+self.trigY((self.BACKPOINTLENGTH),self.degree + self.BACKLEFTDEGREE)

    def getBackRightPoint(self):
        return (self.pos[0]+self.trigX((self.BACKPOINTLENGTH),self.degree + self.BACKRIGHTDEGREE)),self.pos[1]+self.trigY((self.BACKPOINTLENGTH),self.degree + self.BACKRIGHTDEGREE)

    def getFrontCenterPoint(self):
        return (self.pos[0]+self.trigX(self.SIZE[1]/2,self.degree)) , (self.pos[1]+self.trigY(self.SIZE[1]/2, self.degree))

    def updateShipDraw(self):
        self.tri = (self.getFrontCenterPoint(),self.getBackLeftPoint(),self.getBackRightPoint())
