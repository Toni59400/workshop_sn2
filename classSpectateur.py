import pygame

class Spectateur:
    def __init__(self, game,screen, pixel):
        """Class des specateurs
        param : screen - pygame Object - l'écran sur lequel on affiche
                pixel - tuple - la dimension d'un pixel (largeur, hauteur)"""
        self.screen = screen
        self.game = game
        self.pixel = pixel
        self.imgOrigin = pygame.transform.scale(pygame.image.load('assets/spectateur/spectateur.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.img = self.imgOrigin

    def update(self):
        """cette fonction met à jour l'affichage et la position des spectateurs"""
        self.screen.blit(self.img, (0,0))
    
    def zoom(self, n):
        self.img.set_alpha(255-n*(-4.25))