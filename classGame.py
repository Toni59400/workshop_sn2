import pygame
from classPresentateur import Presentateur

from classSpectateur import Spectateur

class Game:
    def __init__(self, screen):
        """
        screen - pygame.Screen - l'écran sur lequel s'affiche le jeu"""
        self.screen = screen
        self.pixel = (self.screen.get_width()/384, self.screen.get_height()/216)
        self.background = pygame.transform.scale(pygame.image.load('assets/background.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.spectateur = Spectateur(self, self.screen, self.pixel)
        self.presentateur = Presentateur(self, self.screen, self.pixel)
        #exemple son
        #self.soundEnd = pygame.mixer.Sound("jeuPingPong/assets/sound/applaudissements.mp3")




        
       
    def update(self):
        self.screen.blit(self.background,(0,0))
        self.spectateur.update()
        self.presentateur.update()


        



