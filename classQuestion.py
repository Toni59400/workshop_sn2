import pygame

class Question():
    '''
    
    '''
    def __init__(self, game, screen, question, reponse, propositions, explication):
        self.screen = screen 
        self.question = question #string
        self.reponse = reponse #index dans la liste proposition
        self.propositions = propositions #liste de propositions
        self.explication = explication #string
        self.game = game
        self.pixel = game.pixel
        self.img = pygame.transform.scale(pygame.image.load('assets/presentateur/bulle.png'),(384*self.pixel[0],216*self.pixel[1]))

    def update(self):
        """cette fonction met à jour l'affichage et la position des spectateurs"""
        self.screen.blit(self.img, (0,0))

    