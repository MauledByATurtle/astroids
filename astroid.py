import pygame
import random
import math

class Astroid:

    def __init__(self, x, y, size = random.randint(50,100)):
        self.pos = [x,y]
        self.size = size
        self.pointsMagnitude = [[0,22.5],[0,67.5],[0,112.5],[0,157.5],[0,202.5],[0,247.5],[0,292.5],[0,337.5]]
        self.drawPoints = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]

        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.rotationalVelocity = 0 #0.05
        self.deacceleration = 0

        self.rectHeightWidth = 0

        self.MAXVELOCITY = 10
        self.SIZEVARIATION = 10
        self.COLOR = (255,255,255)

        self.initPoints()
        self.calculateRectangle()

    def calculateRectangle(self):
        heightWidth = 0
        heightWidth = self.calcSpecificPoint(self.pointsMagnitude)

        self.rectHeightWidth = heightWidth

        self.updateRectangle()

        #################################

    def onSegment(self, p,q,r):
        if(q[0] <= max(p[0], r[0]) and q[0] >= min(p[0],r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1],r[1])):
            return True
        return False

    def orientation(self, p,q,r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

        if(val == 0):
            return 0

        if val > 0:
            return 1
        
        if val < 0:
            return 2

    def doIntersect(self, p1, q1, p2, q2):

        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)

        if(o1 != o2 and o3 != o4):
            return True

        if(o1 == 0 and self.onSegment(p1, p2, q1)):
            return True

        if(o2 == 0 and self.onSegment(p1, q2, q1)):
            return True

        if(o3 == 0 and self.onSegment(p2, p1, q2)):
            return True

        if(o4 == 0 and self.onSegment(p2, q1, q2)):
            return True

        return False

    def checkIntersect(self,shot):
        shotPointA = shot.pos
        shotPointB = shot.posB
        for i in range(len(self.drawPoints)):
            k = (i+1) % (len(self.drawPoints))
            if self.doIntersect(self.drawPoints[i], self.drawPoints[k], shotPointA,  shotPointB):
                self.hit(i,k,shot)

    def calcHit(self, point, shot):
        if(self.pointsMagnitude[point][0] - shot.damage > 0):
            self.pointsMagnitude[point][0] = self.pointsMagnitude[point][0] - shot.damage
        else:
            self.pointsMagnitude[point][0] = 0
            #Destroy

    def calcDamage():
        self.calcAngle()

    def calcAngle():
        adj = point

    def hit(self, pointA, pointB, shot):
        #self.calcDamage()
        self.calcHit(pointA, shot)
        self.calcHit(pointB, shot)
        self.calculateRectangle()

        ####################################

    def updateRectangle(self):
        self.mainRect = pygame.Rect(self.pos[0] - self.rectHeightWidth, self.pos[1] - self.rectHeightWidth , self.rectHeightWidth*2, self.rectHeightWidth*2)
            
    def calcSpecificPoint(self, points):
        heightWidth = 0
        for point in points:
            if point[0] > heightWidth:
                heightWidth = point[0]

        return heightWidth

    def initPoints(self):
        for point in self.pointsMagnitude:
            point[0] = self.varyPoint(point[0],random.randint(-self.SIZEVARIATION,self.SIZEVARIATION))

    def varyPoint(self, singlePoint, change):
        point = singlePoint
        point = self.size + change
        return point
    
    def update(self, clock, size, shotArray):
        self.updatePhysics(clock, size)
        self.updateAstroidDraw()
        self.updateRectangle()

        #######
        for shot in shotArray:
            self.checkIntersect(shot)

    def draw(self, surface):
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
        pygame.draw.rect(surface, (255,0,0), self.mainRect, 1)

    def trigX(self,length,deg):
        return length*math.cos(math.radians(deg))

    def trigY(self,length,deg):
        return length*math.sin(math.radians(deg))
