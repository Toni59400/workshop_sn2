import pygame
from random import randint

class Presentateur:
    def __init__(self, game,screen, pixel):
        """Class des specateurs
        param : screen - pygame Object - l'écran sur lequel on affiche
                pixel - tuple - la dimension d'un pixel (largeur, hauteur)"""
        self.screen = screen
        self.game = game
        self.pixel = pixel
        self.phaseAnim = "attente"
        self.compteurAnim = 0
        self.imgOrigin = {"attente":
            [pygame.transform.scale(pygame.image.load('assets/presentateur/presentateur0.png'),(384*self.pixel[0],216*self.pixel[1])), 
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateur1.png'),(384*self.pixel[0],216*self.pixel[1]))],
            "animation0":[pygame.transform.scale(pygame.image.load('assets/presentateur/presentateur0.0.png'),(384*self.pixel[0],216*self.pixel[1])), 
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateur0.1.png'),(384*self.pixel[0],216*self.pixel[1])), 
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateur0.2.png'),(384*self.pixel[0],216*self.pixel[1])), 
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateur0.3.png'),(384*self.pixel[0],216*self.pixel[1])), 
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateur0.4.png'),(384*self.pixel[0],216*self.pixel[1]))],
            "parle":[pygame.transform.scale(pygame.image.load('assets/presentateur/presentateurParle0.png'),(384*self.pixel[0],216*self.pixel[1])),
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateurParle1.png'),(384*self.pixel[0],216*self.pixel[1])),
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateurParle2.png'),(384*self.pixel[0],216*self.pixel[1])),
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateurParle3.png'),(384*self.pixel[0],216*self.pixel[1])),
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateurParle4.png'),(384*self.pixel[0],216*self.pixel[1])),
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateurParle5.png'),(384*self.pixel[0],216*self.pixel[1])),
            pygame.transform.scale(pygame.image.load('assets/presentateur/presentateurParle6.png'),(384*self.pixel[0],216*self.pixel[1]))]
        }
        self.img = self.imgOrigin[self.phaseAnim][self.compteurAnim]

    def update(self):
        """cette fonction met à jour l'affichage et la position des spectateurs"""
        #calcul du pixel
        self.pixel = (self.screen.get_width()/384, self.screen.get_height()/216)
        
        if self.phaseAnim=="attente":
            if self.game.compteur % 10 == 0:
                if randint(0,20) == 0: #mettre l'animation miroir
                    self.phaseAnim = "animation0"
                    self.sensAnim = 1
                    self.compteurAnim = 0
                if self.compteurAnim not in [0,1]:
                    self.compteurAnim = 0
                self.compteurAnim = int(not bool(self.compteurAnim))
                self.img =self.img = self.imgOrigin[self.phaseAnim][self.compteurAnim]
                self.zoom(self.game.zoom)
        elif self.phaseAnim=="parle":
            if self.game.compteur %2 == 0:
                self.compteurAnim = randint(0,6)
                self.img = self.imgOrigin[self.phaseAnim][self.compteurAnim]
                self.zoom(self.game.zoom)
        elif self.phaseAnim == "animation0":
            if self.game.compteur %3 == 0:
                if self.sensAnim == 1:
                    self.compteurAnim +=1
                    if self.compteurAnim == 4:
                        self.sensAnim = 0
                else:
                    self.compteurAnim -= 1
                    if self.compteurAnim == -1:
                        self.phaseAnim = "attente"
                print(self.compteurAnim)
                self.img = self.imgOrigin[self.phaseAnim][self.compteurAnim]
                self.zoom(self.game.zoom)
        self.screen.blit(self.img, (self.pixel[0]*192 - self.img.get_width()/2, self.pixel[1]*108 - self.img.get_height()/2 + 40*self.pixel[1]/100*self.game.zoom))
        
    def zoom(self, n):
        self.img = pygame.transform.rotozoom(self.imgOrigin[self.phaseAnim][self.compteurAnim],0,1+(n*(2.5/255)))
        if n > 50:
            self.img.set_alpha(255-(n-50)*12.75)

    def parle(self):
        pass