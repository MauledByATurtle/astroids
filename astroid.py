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
        self.rotationalVelocity = 0
        self.deacceleration = 0

        self.rectHeightWidth = 0

        self.MAXVELOCITY = 10
        self.SIZEVARIATION = size*0.5
        self.COLOR = (255,255,255)
        self.ROTATIONALSPEED = 0.001
        self.OFFSCREENBUFFER = self.size
        self.initPoints()
        self.calculateRectangle()

        self.amHit = False

    def calculateRectangle(self):
        heightWidth = self.calcSpecificPoint(self.pointsMagnitude)
        self.rectHeightWidth = heightWidth
        self.updateRectangle()

        #################################

    def checkHit(self, shotArray, ship):
        for shot in shotArray:
            if(self.mainRect.collidepoint(shot.pos)):
                self.checkIntersect(shot, ship)

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

    def checkIntersect(self, shot, ship):
        shotPointA = shot.pos
        shotPointB = shot.posC
        
        for i in range(len(self.drawPoints)):
            k = (i+1) % (len(self.drawPoints))
            if self.doIntersect(self.drawPoints[i], self.drawPoints[k], shotPointA,  shotPointB):
                self.hit(i,k,shot, ship) 

    def calcHit(self, point, shot, damagePerc):

        if((self.pointsMagnitude[point][0] - (shot.damage * damagePerc)) > 0):
            self.pointsMagnitude[point][0] = self.pointsMagnitude[point][0] - (shot.damage * damagePerc)
            self.amHit = True
        else:
            self.pointsMagnitude[point][0] = 0
            #Destroy

    def calcDamage(self, pointA, pointB, shot):
        damage = [0,0]
        distanceBetweenPoints = abs(self.calcDistance(pointA, pointB))
        damage[0] = 1 - abs(self.calcDistance(pointA, shot.pos)) / distanceBetweenPoints
        damage[1] = 1 - abs(self.calcDistance(pointB, shot.pos)) / distanceBetweenPoints
        return damage

    def hit(self, pointA, pointB, shot, ship):
        self.calcShotVelocityAndSpin(self.drawPoints[pointA], self.drawPoints[pointB], shot)
        damage = self.calcDamage(self.drawPoints[pointA],self.drawPoints[pointB],shot)
        self.calcHit(pointA, shot, abs(damage[0]))
        self.calcHit(pointB, shot, abs(damage[1]))
        ship.deleteShot(shot)
        self.calculateRectangle()

    def calcDistance(self, pointA, pointB):
        return math.sqrt(math.pow(pointB[0]-pointA[0],2) + math.pow(pointB[1]-pointA[1],2))


        ####################################

    def calcShotVelocityAndSpin(self, pointA, pointB, shot):
        shotAngle = self.calcShotAngle(pointA, pointB, shot)
        angular = self.trigX(shotAngle, shot.force)
        velocity = self.trigY(shotAngle, shot.force)
        velocityDirection = shot.degree

        #
        self.rotationalVelocity -= angular * self.ROTATIONALSPEED
        print(self.trigX(shot.force,shot.degree))
        self.velocity[0] += self.trigX(shot.force,shot.degree) + (self.trigX(velocity, velocityDirection)*0.1)
        self.velocity[1] += self.trigY(shot.force,shot.degree) + (self.trigY(velocity, velocityDirection)*0.1)
        


    def calcShotAngle(self, pointA, pointB, shot):
        shotSlope = self.calcSlope(shot.pos, shot.posB)
        octSlope = self.calcSlope(pointA, pointB)
        topHalf = octSlope -  shotSlope
        bottomHalf = 1 + (octSlope * shotSlope)

        return( math.degrees(math.atan(topHalf/bottomHalf)))


    def calcSlope(self, pointA, pointB):
        adj = pointB[0] - pointA[0]
        opp = pointB[1] - pointA[1]
        try:
            slope = opp/adj
        except ZeroDivisionError:
            print("RareCase of a slope of 0")
            
        return opp/adj

        ####################################

    def changeAngles(self, newList):
        self.pointsMagnitude = newList

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
    
    def update(self, clock, size):
        self.updatePhysics(clock, size)
        self.updateAstroidDraw()
        self.updateRectangle()

    def draw(self, surface):
        self.drawAstroid(surface)

    def updatePhysics(self, clock, size):
        self.checkAllBounds(size)
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
        pygame.draw.polygon(surface, (50,50,50), self.drawPoints, 1)
        #pygame.draw.rect(surface, (255,0,0), self.mainRect, 1)

    def trigX(self,length,deg):
        return length*math.cos(math.radians(deg))

    def trigY(self,length,deg):
        return length*math.sin(math.radians(deg))

    def checkAllBounds(self, size):
        self.checkBoundTop(size[1], size[0])
        self.checkBoundBot(size[1], size[0])
        self.checkBoundRight(size[0], size[1])
        self.checkBoundLeft(size[0], size[1])

    def checkBoundTop(self, height, width):
        if self.pos[1] > height + self.OFFSCREENBUFFER:
            self.pos[1] = -self.OFFSCREENBUFFER
            self.pos[0] = width - self.pos[0]

    def checkBoundBot(self, height, width):
        if self.pos[1] < -self.OFFSCREENBUFFER:
            self.pos[1] = height + self.OFFSCREENBUFFER
            self.pos[0] = width - self.pos[0]

    def checkBoundRight(self, width, height):
        if self.pos[0] > width + self.OFFSCREENBUFFER:
            self.pos[0] = -self.OFFSCREENBUFFER
            self.pos[1] = height - self.pos[1]

    def checkBoundLeft(self, width, height):
        if self.pos[0] < -self.OFFSCREENBUFFER:
            self.pos[0] = width + self.OFFSCREENBUFFER
            self.pos[1] = height - self.pos[1]
