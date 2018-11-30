import pygame
import ship
import keyboard
import shot_basic
import astroid
import basic_font
from pygame.locals import *

#Bugs:


#TODO:
    #particle class
    #ship hit detection
    #menus

class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 920
        self.gameClock = pygame.time.Clock()
        self.mainMenu = True
        self.mainMenuTimer = 20
        self.menuCounter = 0

    def on_game_init(self):
        self.astroid = astroid.Astroid(500,500,30)
        self.debugText = basic_font.basic_Text()
        self.debugText.setTopLeft(0,0)

    def on_init(self):
        
        pygame.init()
        pygame.font.init()
        
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.player = ship.Ship(self.width/1.5,self.height/1.5)
        self.keyboard = keyboard.Keyboard()
        
        self.mainMenuFont = basic_font.basic_Text()
        self.mainMenuFont.setCenter(self.width/2-50, self.height/3)
        self.mainMenuFont.setText("Main Menu")

        self.playFont = basic_font.basic_Text()
        self.playFont.setCenter(self.width/2-20, self.height/2)
        self.playFont.setColor((0,0,0))
        self.playFont.setText("Play")
        
        self.playAstroid = astroid.Astroid(self.width/2, self.height/2, 0)
        self.playAstroid.changeAngles([[67,22.5],[35,67.5],[42,112.5],[60,157.5],[52,202.5],[31,247.5],[33,292.5],[62,337.5]])
        self.playAstroid.calculateRectangle()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            self.mainMenu = False
        self.keyboard.keyDown(event)
        self.keyboard.keyUp(event)
            
    def on_loop(self):
        
        self.astroid.update(self.gameClock, self.size)
        self.astroid.checkHit(self.player.bulletsArray, self.player)
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player_update()
        self.player.draw(self._display_surf)
        self.astroid.draw(self._display_surf)
        #
        self.debugText.setText(str(self.gameClock.get_fps()))
        self.debugText.printText(self._display_surf)
    
    def on_cleanup(self):
        pygame.quit()

    def player_update(self):
        self.player.update(self.keyboard, self.gameClock, self.size)
        self.player.updateShots(self._display_surf, self.keyboard, self.gameClock, self.size)

    def menuRender(self):
        
        self.player.draw(self._display_surf)
        self.playAstroid.draw(self._display_surf)
        self.playFont.printText(self._display_surf)
        self.mainMenuFont.printText(self._display_surf)

    def menuLoop(self):
        self._display_surf.fill((0,0,0))
        self.player_update()
        
        self.playAstroid.update(self.gameClock, self.size)
        self.playAstroid.checkHit(self.player.bulletsArray, self.player)

        self.playFont.setCenter(self.playAstroid.pos[0],self.playAstroid.pos[1])

        if(self.playAstroid.amHit == True):
            self.menuCounter += 1

        if(self.menuCounter >= self.mainMenuTimer):
            self.mainMenu = False

    def on_execute(self):

        if self.on_init() == False:
            self._running = False

        while( self.mainMenu == True):
            for event in pygame.event.get():
                self.on_event(event)
            self.menuLoop()
            self.menuRender()
            pygame.display.update()

        self.on_game_init()

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.display.update()
            
        self.on_cleanup()

if __name__ == "__main__" :
    game = Game()
    game.on_execute()
