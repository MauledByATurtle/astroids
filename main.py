import pygame
import ship
import keyboard
import shot_basic
import astroid
from pygame.locals import *

class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 920
        self.gameClock = pygame.time.Clock()

    def on_init(self):
        self.player = ship.Ship(self.width/2,self.height/2)
        self.keyboard = keyboard.Keyboard()

        self.astroid = astroid.Astroid(500,500,20)
        
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        #self._running = True

        #
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Ariel', 30)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        self.keyboard.keyDown(event)
        self.keyboard.keyUp(event)
            
    def on_loop(self):
        if(self.keyboard.getW()):
            pass
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.update(self._display_surf, self.keyboard, self.gameClock, self.size)
        self.player.updateShots(self._display_surf, self.keyboard, self.gameClock, self.size)

        self.astroid.update(self._display_surf, self.gameClock, self.size)
        #
        textsurface = self.myfont.render(str(self.gameClock.get_fps()), False, (255,255,255))
        self._display_surf.blit(textsurface,(0,0))
    
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

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
