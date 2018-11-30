import pygame

class basic_Text:
    def __init__(self, color = (255,255,255), size = 20):
        pygame.font.init()
        self.pos = [0,0]
        self.text = ""
        self.size = size
        self.color = color
        self.font = pygame.font.Font('AmaticSC-Regular.ttf', 30)
        self.textRender = self.font.render(self.text, False, self.color)
        self.rect = self.textRender.get_rect(center =(self.pos[0],self.pos[1]))

    def printText(self, surface):
        surface.blit(self.textRender, self.rect)

    def setCenter(self, x, y):
        self.pos[0] = x
        self.pos[1] = y
        self.rect = self.textRender.get_rect(center =(self.pos[0],self.pos[1]))

    def setTopLeft(self,x,y):
        self.pos[0] = x
        self.pos[1] = y
        self.rect = self.textRender.get_rect(topleft =(self.pos[0],self.pos[1]))

    def setText(self, newText):
        self.text = newText
        self.textRender = self.font.render(self.text, False, self.color)

    def setColor(self, newColor):
        self.color = newColor
    
