import pygame

class Game:
    def __init__(self, screen, difficulty):
        """
        screen - pygame.Screen - l'écran sur lequel s'affiche le jeu
        difficulty - int - le niveau de difficulté entre 1 et 3"""
        self.difficulty = difficulty
        self.screen = screen
        self.pixel = self.screen.get_width()/400
        self.background = pygame.transform.scale(pygame.image.load('jeuPingPong/assets/background.png'),(400*self.pixel,400*self.pixel))
        #exemple son
        #self.soundEnd = pygame.mixer.Sound("jeuPingPong/assets/sound/applaudissements.mp3")




        
       
    def update(self):
        pass


        



