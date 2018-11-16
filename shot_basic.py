import pygame
import math

class ShotBasic:
    def __init__(self, x, y, angle):
        self.pos = [x,y]
        self.posB = [0,0]
        self.posC = [0,0]
        self.color = (255,0,0)
        self.degree = angle
        self.speed = 30
        self.length = 10
        self.hitDectLen = self.speed * 2
        self.width = 2
        self.damage = 10
        self.force = 1

    def update(self, surface, clock):
        self.updatePhysics(clock)
        self.updateBulletDraw()
        pygame.draw.line(surface, (255,0,0), self.pos, self.posB, self.width)

    def updateBulletDraw(self):
        self.posC[0] = self.pos[0]+self.trigX(self.hitDectLen,self.degree)
        self.posC[1] = self.pos[1]+self.trigY(self.hitDectLen,self.degree)
        self.posB[0] = self.pos[0]+self.trigX(self.length,self.degree)
        self.posB[1] = self.pos[1]+self.trigY(self.length,self.degree)
        
    def updatePhysics(self, clock):
        self.pos[0] = (self.pos[0] + self.trigX(self.speed,self.degree))
        self.pos[1] = (self.pos[1] + self.trigY(self.speed,self.degree))

    def trigX(self,length,deg):
        return length*math.cos(math.radians(deg))

    def trigY(self,length,deg):
        return length*math.sin(math.radians(deg))

    def checkAllBounds(self, size):
        if self.checkBoundTop(size[1]) or self.checkBoundBot(size[1]) or self.checkBoundRight(size[0]) or self.checkBoundLeft(size[0]):
            return True
        else:
            return False

    def checkBoundTop(self, height):
        if self.pos[1] > height:
            return True
        else:
            return False

    def checkBoundBot(self, height):
        if self.pos[1] < 0:
            return True
        else:
            return False

    def checkBoundRight(self, width):
        if self.pos[0] > width:
            return True
        else:
            return False

    def checkBoundLeft(self, width):
        if self.pos[0] < 0:
            return True
        else:
            return False
