import pygame

class Ecran:
    def __init__(self, game,screen, pixel):
        """Class des specateurs
        param : screen - pygame Object - l'écran sur lequel on affiche
                pixel - tuple - la dimension d'un pixel (largeur, hauteur)"""
        self.screen = screen
        self.game = game
        self.pixel = pixel
        self.imgOrigin = pygame.transform.scale(pygame.image.load('assets/ecran/ecran.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.img = self.imgOrigin

    def update(self):
        """cette fonction met à jour l'affichage et la position des spectateurs"""
        self.screen.blit(self.img, (self.pixel[0]*192 - self.img.get_width()/2, self.pixel[1]*108 - self.img.get_height()/2 + 68*self.pixel[1]/100*self.game.zoom))

    def zoom(self, n):
        self.img = pygame.transform.rotozoom(self.imgOrigin,0,1+(n*(2.5/255)))