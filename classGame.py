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
        self.n_question = 8
        self.pixel = (self.screen.get_width()/384, self.screen.get_height()/216)
        self.background = pygame.transform.scale(pygame.image.load('assets/background.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.spectateur = Spectateur(self, self.screen, self.pixel)
        self.presentateur = Presentateur(self, self.screen, self.pixel)
        self.ecran = Ecran(self, self.screen, self.pixel)
        self.zoom = 0 #entre 0 et 100
        self.compteurAnim = 0
        self.phase = "question"
        self.compteur = 0
        #exemple son
        #self.soundEnd = pygame.mixer.Sound("jeuPingPong/assets/sound/applaudissements.mp3")
        #Creationliste des question
        dict_question = [{"question": "Les personnes entièrement vaccinées développent le syndrome d’immunodéficience acquise (sida).", "r1" : "Vrai", "r2" : "Faux", "bonne_reponse" : 2, "explication" : "Cette FakeNews provient du site 'Le Grand Réveil', et elle aurait pour source : 'Les rapports officiels du gouvernement britanique'"},
                        {"question": "Le vaccin contre le Covid-19 contiendrait des puces électroniques 5G, pour nous tracer et ficher !", "r1" : "Vrai", "r2": "Faux", "bonne_reponse" : 2, "explication" : " Cette FakeNews est relayer sur les reseaux, démentie par le CHU de Toulouse dans un tweet."},
                        {"question":"L'exploration spatiale est elle possible grâce aux financements des organisations de protection de l'environnement ?", "r1":"vrai", "r2":"faux", "bonne_reponse": 1 , "explication":"LEs associations veulent quitter la Terre car on ne pourra pas la sauver"},
                        {"question":"Pourquoi y a t-il des années bisextiles?", "r1":"A cause de la rotation de la planète autour du soleil", "r2":"Pour combler les pertes financières des banques mondiales", "bonne_reponse": 1, "explication":"nous ne pouvons laisser passé de tels déficit, c'est pour cela qu'on a créé les années bisextiles"},
                        {"question":"Y a t-il un dinosaure ayant résisté aux météorites?", "r1":"Oui", "r2":"Non", "bonne_reponse": 1 , "explication":"Oui pour rappel les poules sont des dinosaures puisque c'est le seul volatile à avoir des dents"},
                        {"question":"Qui invente les maladies que nous connaissons ?", "r1":"La nature", "r2":"Les lobbys pharmaceutique", "bonne_reponse": 2 , "explication":"Ils préfèrent effectivement s'enrichir en innovant ainsi pour que leurs propres vaccins soit mis en avant sur le marché"},
                        {"question":"Quel vaccin contient des puces 5g ?", "r1":"Le vaccin contre la grippe", "r2":"Le vaccin contre la COVID", "bonne_reponse": 2 , "explication":"Les Nations Unis ont obligés les laboratoires à implanter des puces 5G pour contrôler nos opinions politiques"},
                        {"question":"Quel fût le dernier crime commis par la haute église ?", "r1":"L'arrivée de Jésus sur Terre", "r2":"Le pape est impliqué dans un traffique d'enfant", "bonne_reponse": 2 , "explication":"Nous savons que Dieu n'existe pas voyons"},
                        {"question":"Quel évènement les USA ont perpétré pour entammer une sois disant guerre contre le terrorisme ?", "r1":"Le 11 Septembre", "r2":"La restauration de Walt Disney", "bonne_reponse": 1 , "explication":"En effet le différent entre Ben Laden et Georges W Bush vient du fait que Ben Laden a gagné un tournoi d'échec contre Bush et ce dernier souhaita prendre sa revanche"},
                        {"question":"Est-ce que l'univers est constitué uniquement de la voie lactée ?", "r1":"oui", "r2":"non", "bonne_reponse": 1 , "explication":"Il n'y a rien d'autres que la voie lactée, sinon nous aurions eu la visite d'autres civilisations"},
                        {"question":"Qu'est-ce qui a été inventé pour séparer les Hommes ?", "r1":"Les Langues étrangères", "r2":"Les murs", "bonne_reponse":1 , "explication":"Les langues étrangères ont été créées uniquement pour que les Hommes soient en discorde constente et que l'industrie militaire puisse en profiter"}
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
        self.compteur += 1
        if self.phase == "dezoom" :
            if self.zoom>0:
                self.updateZoom(self.zoom-5)
            else : 
                self.phase = "explication"
                self.presentateur.parle()
        if self.phase == "zoom" : 
            if self.zoom < 100:
                self.updateZoom(self.zoom+5)
            else : 
                self.phase = self.rep

        
            
        self.screen.blit(self.background,(0,0))
        
        self.ecran.update()
        self.spectateur.update()
        self.presentateur.update()
        self.lst_obj_question[self.n_question].update()
    
    def eventCarreGauche(self):
        """
        Dans ce carré se trouve toujours la reponse 1 (rep1) du dictionnaire.
        """
        choix = 1

        if self.lst_obj_question[self.n_question].reponse == choix : 
            self.phase = "zoom"
            self.rep = "animBonneRep"
        else:
            self.phase = "zoom"
            self.rep = "animMauvaiseRep"
    
    def eventCarreDroite(self):
        """
        Dans ce carré se trouve toujours la reponse 2 (rep2) du dictionnaire.
        """
        choix = 2
        if self.lst_obj_question[self.n_question].reponse == choix : 
            self.phase = "zoom"
            self.rep = "animBonneRep"
        else:
            self.phase = "zoom"
            self.rep = "animMauvaiseRep"

    def animationBonneReponse(self):
        self.phase = "animBonRep"

    def animationMauvaiseReponse(self):
        self.phase = "animBonRep"

    def resize(self):
        """cette fonction recalcule les dimensions de tout les elements si la taille est modifiée"""
        #calcul du pixel
        self.pixel = (self.screen.get_width()/384, self.screen.get_height()/216)
        self.presentateur.pixel = (self.screen.get_width()/384, self.screen.get_height()/216)
        self.spectateur.pixel = self.pixel
        self.ecran.pixel = self.pixel

        #images
        self.background = pygame.transform.scale(pygame.image.load('assets/background.png'),(384*self.pixel[0],216*self.pixel[1]))

        self.spectateur.imgOrigin = pygame.transform.scale(pygame.image.load('assets/spectateur/spectateur.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.spectateur.img = pygame.transform.scale(self.spectateur.img,(384*self.pixel[0],216*self.pixel[1]))

        #redefinition des images de l'écran
        self.ecran.img = pygame.transform.scale(self.ecran.img,(384*self.pixel[0],216*self.pixel[1]))
        self.ecran.imgOrigin = {'attente':[
                pygame.transform.scale(pygame.image.load('assets/ecran/ecran0.png'),(384*self.pixel[0],216*self.pixel[1])),
                pygame.transform.scale(pygame.image.load('assets/ecran/ecran1.png'),(384*self.pixel[0],216*self.pixel[1]))],
            'bonneRep':[
                pygame.transform.scale(pygame.image.load('assets/ecran/ecranRight0.png'),(384*self.pixel[0],216*self.pixel[1])),
                pygame.transform.scale(pygame.image.load('assets/ecran/ecranRight1.png'),(384*self.pixel[0],216*self.pixel[1])),
                pygame.transform.scale(pygame.image.load('assets/ecran/ecranRight2.png'),(384*self.pixel[0],216*self.pixel[1]))
            ],
            'mauvaiseRep':[
                pygame.transform.scale(pygame.image.load('assets/ecran/ecranWrong0.png'),(384*self.pixel[0],216*self.pixel[1])),
                pygame.transform.scale(pygame.image.load('assets/ecran/ecranWrong1.png'),(384*self.pixel[0],216*self.pixel[1])),
                pygame.transform.scale(pygame.image.load('assets/ecran/ecranWrong2.png'),(384*self.pixel[0],216*self.pixel[1]))
            ]
        }
        self.ecran.imgOriginStructure = pygame.transform.scale(self.ecran.imgOriginStructure,(384*self.pixel[0],216*self.pixel[1]))
        self.ecran.imgStructure = pygame.transform.scale(pygame.image.load('assets/ecran/structure.png'),(384*self.pixel[0],216*self.pixel[1]))

        self.presentateur.imgOrigin = pygame.transform.scale(pygame.image.load('assets/presentateur/presentateur.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.presentateur.img = pygame.transform.scale(self.presentateur.imgOrigin,(384*self.pixel[0],216*self.pixel[1]))

        for k in self.lst_obj_question:
            k.pixel = self.pixel
            k.img = pygame.transform.scale(pygame.image.load('assets/presentateur/bulle.png'),(384*self.pixel[0],216*self.pixel[1]))
            k.reponse1 = pygame.transform.scale(pygame.image.load('assets/presentateur/carreRep.png'), (96*self.pixel[0], 64*self.pixel[1]))
            k.reponse2 = pygame.transform.scale(pygame.image.load('assets/presentateur/carreRep.png'), (96*self.pixel[0], 64*self.pixel[1]))
            k.arial_font = pygame.font.SysFont("arial", round(8*self.pixel[1]))
            k.rectangle = pygame.draw.rect(k.screen, k.white, pygame.Rect(30*self.pixel[0], 25*self.pixel[1], 250*self.pixel[0], 68*self.pixel[1]), width=0)


