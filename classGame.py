from turtle import update
import pygame
from classPresentateur import Presentateur
from classEcran import Ecran
from classQuestion import Question
from classSpectateur import Spectateur

class Game:
    def __init__(self, screen):
        """
        screen - pygame.Screen - l'écran sur lequel s'affiche le jeu"""
        self.screen = screen
        self.n_question = 0
        self.pixel = (self.screen.get_width()/384, self.screen.get_height()/216)
        self.background = pygame.transform.scale(pygame.image.load('assets/background.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.spectateur = Spectateur(self, self.screen, self.pixel)
        self.presentateur = Presentateur(self, self.screen, self.pixel)
        self.ecran = Ecran(self, self.screen, self.pixel)
        self.zoom = 0 #entre 0 et 100
        #exemple son
        #self.soundEnd = pygame.mixer.Sound("jeuPingPong/assets/sound/applaudissements.mp3")
        #Creationliste des question
        dict_question = [{"question": "Les personnes entièrement vaccinées développent le syndrome d’immunodéficience acquise (sida).", "r1" : "Vrai", "r2" : "Faux", "bonne_reponse" : 2, "explication" : "Cette FakeNews provient du site 'Le Grand Réveil', et elle aurait pour source : 'Les rapports officiels du gouvernement britanique'"},
                 {"question": "Le vaccin contre le Covid-19 contiendrait des puces électroniques 5G, pour nous tracer et ficher !", "r1" : "Vrai", "r2": "Faux", "bonne_reponse" : 2, "explication" : " Cette FakeNews est relayer sur les reseaux, démentie par le CHU de Toulouse dans un tweet."}
                ]

        self.lst_obj_question = []

        for i in dict_question : 
            self.lst_obj_question.append(Question( self ,screen,  i['question'], i["bonne_reponse"], [i['r1'], i['r2']], i['explication']))

    def updateZoom(self, n):
        self.zoom = n
        self.spectateur.zoom(n)
        self.ecran.zoom(n)
        self.presentateur.zoom(n)
        
    def update(self):
        #if self.zoom < 100:
        #    self.updateZoom(self.zoom+3)
        self.screen.blit(self.background,(0,0))
        
        self.ecran.update()
        self.spectateur.update()
        self.presentateur.update()
        self.lst_obj_question[0].update()
        

