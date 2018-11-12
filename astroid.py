import pygame
import random
import math

class Astroid:

    def __init__(self, x, y, size = random.randint(50,100)):
        self.pos = [x,y]
        self.size = size
        self.pointsMagnitude = [[0,22.5],[0,67.5],[0,112.5],[0,157.5],[0,202.5],[0,247.5],[0,292.5],[0,337.5]]
        self.drawPoints = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]

        self.velocity = [1,1]
        self.acceleration = [0,0]
        self.rotationalVelocity = 0.05

        self.deacceleration = 0

        self.MAXVELOCITY = 10
        self.SIZEVARIATION = 10
        self.COLOR = (255,255,255)

        self.initPoints()

    def initPoints(self):
        for point in self.pointsMagnitude:
            point[0] = self.varyPoint(point[0])

    def varyPoint(self, singlePoint):
        point = singlePoint
        point = self.size + random.randint(-self.SIZEVARIATION,self.SIZEVARIATION)
        return point
    
    def update(self, surface, clock, size):
        self.updatePhysics(clock, size)
        self.updateAstroidDraw()
        self.drawAstroid(surface)

    def updatePhysics(self, clock, size):
        self.updateVelocity()
        self.updateRotation(clock)

    def updateVelocity(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.velocity[0] = self.updateVelocityParamater(self.velocity[0])
        self.velocity[1] = self.updateVelocityParamater(self.velocity[1])
            
    def updateVelocityParamater(self,velocityXorY):
        if velocityXorY < -self.MAXVELOCITY:
            velocityXorY = -self.MAXVELOCITY
            
        if velocityXorY > self.MAXVELOCITY:
            velocityXorY = self.MAXVELOCITY

        if abs(velocityXorY) > 0:
            if velocityXorY > 0:
                velocityXorY -= self.deacceleration
                if velocityXorY < 0:
                    velocityXorY = 0
            elif velocityXorY < 0:
                velocityXorY += self.deacceleration
                if velocityXorY > 0:
                    velocityXorY = 0

        return velocityXorY

    def updateRotation(self,clock):
        time = clock.tick(60)
        for point in self.pointsMagnitude:
            point[1] += self.rotationalVelocity  * time

    def updateAstroidDraw(self):
        for i in range(len(self.drawPoints)):
            pointX = self.pos[0] + self.trigX(self.pointsMagnitude[i][0],self.pointsMagnitude[i][1])
            pointY = self.pos[1] + self.trigY(self.pointsMagnitude[i][0],self.pointsMagnitude[i][1])
            self.drawPoints[i] = (pointX,pointY)

    def drawAstroid(self, surface):
        pygame.draw.polygon(surface, self.COLOR, self.drawPoints)

    def trigX(self,length,deg):
        return length*math.cos(math.radians(deg))

    def trigY(self,length,deg):
        return length*math.sin(math.radians(deg))
