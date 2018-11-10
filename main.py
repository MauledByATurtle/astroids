import pygame
import ship
import keyboard
from pygame.locals import *

class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 920
        self.gameClock = pygame.time.Clock()

    def on_init(self):
        self.player = ship.Ship(100,100)
        self.keyboard = keyboard.Keyboard()
        
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

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
