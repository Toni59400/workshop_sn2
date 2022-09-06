import pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.pixel = self.screen.get_width()/400
        #self.background = pygame.transform.scale(pygame.image.load('jeuPingPong/assets/background.png'),(400*self.pixel,400*self.pixel))
        
    def update(self):
        pass

class Question():
    '''
    
    '''
    def __init__(self, screen, question, reponse, propositions, explication):
        self.screen = screen 
        self.question = question #string
        self.reponse = reponse #index dans la liste proposition
        self.propositions = propositions #liste de propositions
        self.explication = explication #string