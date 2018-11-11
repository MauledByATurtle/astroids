import pygame

class Keyboard:

    def __init__(self):
        self.key_w = False
        self.key_a = False
        self.key_s = False
        self.key_d = False
        self.key_space = False


    def keyDown(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.key_w = True
                #print('keyDown_w')
            if event.key == pygame.K_a:
                self.key_a = True
                #print('keyDown_a')
            if event.key == pygame.K_s:
                self.key_s = True
                #print('keyDown_s')
            if event.key == pygame.K_d:
                self.key_d = True
                #print('keyDown_d')
            if event.key == pygame.K_SPACE:
                self.key_space = True
                #print('keyDown_space')

    def keyUp(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.key_w = False
                #print('keyUp_w')
            if event.key == pygame.K_a:
                self.key_a = False
                #print('keyUp_a')
            if event.key == pygame.K_s:
                self.key_s = False
                #print('keyUp_s')
            if event.key == pygame.K_d:
                self.key_d = False
                #print('keyUp_d')
            if event.key == pygame.K_SPACE:
                self.key_space = False
                #print('keyUp_space')

    def getW(self):
        return self.key_w

    def getA(self):
        return self.key_a

    def getS(self):
        return self.key_s

    def getD(self):
        return self.key_d

    def getSpace(self):
        return self.key_space
