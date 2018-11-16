import pygame
import ship
import keyboard
import shot_basic
import astroid
from pygame.locals import *

#Bugs:
    #bullets hitting both sides
    #divison by zero

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

    def on_game_init(self):
        #self.player = ship.Ship(self.width/2,self.height/2)
        self.keyboard = keyboard.Keyboard()

        self.astroid = astroid.Astroid(500,500,30)
        self.myfont = pygame.font.SysFont('Ariel', 30)

    def on_init(self):
        self.player = ship.Ship(self.width/2,self.height/2)
        self.keyboard = keyboard.Keyboard()
        
        pygame.init()
        pygame.font.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.mainMenuFont = pygame.font.SysFont('Ariel', 30)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        self.keyboard.keyDown(event)
        self.keyboard.keyUp(event)
            
    def on_loop(self):
        self._display_surf.fill((0,0,0))
        self.player_update()

        self.astroid.update(self.gameClock, self.size)
        self.astroid.checkHit(self.player.bulletsArray, self.player)
    
    def on_render(self):
        self.player.draw(self._display_surf)
        self.astroid.draw(self._display_surf)
        
        #
        textsurface = self.myfont.render(str(self.gameClock.get_fps()), False, (255,255,255))
        self._display_surf.blit(textsurface,(0,0))
    
    def on_cleanup(self):
        pygame.quit()

    def player_update(self):
        self.player.update(self.keyboard, self.gameClock, self.size)
        self.player.updateShots(self._display_surf, self.keyboard, self.gameClock, self.size)

    def menuRender(self):
        self._display_surf.fill((0,0,0))
        self.player_update()
        self.player.draw(self._display_surf)
        
        titleText = self.mainMenuFont.render("Main Menu", False, (255,255,255))
        self._display_surf.blit(titleText,(self.width/2,self.height/3))

        if self.keyboard.getSpace() == True:
            self.mainMenu = False

    def on_execute(self):

        if self.on_init() == False:
            self._running = False

        while( self.mainMenu == True):
            for event in pygame.event.get():
                self.on_event(event)
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
