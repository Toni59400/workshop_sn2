import pygame

class Presentateur:
    def __init__(self, game,screen, pixel):
        """Class des specateurs
        param : screen - pygame Object - l'écran sur lequel on affiche
                pixel - tuple - la dimension d'un pixel (largeur, hauteur)"""
        self.screen = screen
        self.game = game
        self.pixel = pixel
        self.img = pygame.transform.scale(pygame.image.load('assets/presentateur/presentateur.png'),(384*self.pixel[0],216*self.pixel[1]))

    def update(self):
        """cette fonction met à jour l'affichage et la position des spectateurs"""
        self.screen.blit(self.img, (0,0))
        #changer l'opacité