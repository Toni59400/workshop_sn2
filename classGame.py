import textwrap
import pygame
from classPresentateur import Presentateur
from classEcran import Ecran
from classQuestion import Question
from classSpectateur import Spectateur
from random import choice, randint

class Game:
    def __init__(self, screen):
        """
        screen - pygame.Screen - l'écran sur lequel s'affiche le jeu
        """
        self.bonne_reponse = 0 
        self.finish = False
        self.mauvaise_reponse = 0
        self.screen = screen
        self.pixel = (self.screen.get_width()/384, self.screen.get_height()/216)
        self.background = pygame.transform.scale(pygame.image.load('assets/background.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.spectateur = Spectateur(self, self.screen, self.pixel)
        self.terre_p = pygame.transform.scale(pygame.image.load('assets/terrePlate.png'), (32*self.pixel[0], 32*self.pixel[1]))
        self.terre_r = pygame.transform.scale(pygame.image.load('assets/terreRonde.png'), (32*self.pixel[0], 32*self.pixel[1]))
        self.presentateur = Presentateur(self, self.screen, self.pixel)
        self.ecran = Ecran(self, self.screen, self.pixel)
        self.cadreConseil = pygame.transform.scale(pygame.image.load('assets/cadreConseil.png'), (384*self.pixel[0],216*self.pixel[1]))
        self.zoom = 0 #entre 0 et 100
        self.compteurAnim = 0
        self.phase = "question"
        self.compteur = 0
        self.cinematique = True
        self.textCinematique = "Vous vous réveillez aprés un sommeil de plusieurs siecles, vous avez été améné sur ce plateau afin d'évaluer vos compétences intellectuels. Mais quelque chose semble ne pas tourner rond dans cette nouvelle société. Peut être mieux vaut-il ne pas accorder trop facilement sa confiance pour le moment... \n \n Vous devez répondre aux questions suivantes. Un représentant de \"The mirror\" , le journal qui semble diriger les choses par ici, sera présent sur l'écran derrière vous. Vous avez pus observer quelques uns de leurs articles, et il semble évident que ce torchon n'est pas fiable pour un sous. Il est fort probable qu'il réagisse mal face aux vérités..."
        self.textCinematiqueDefeat = "Vous avez été assimilé par cette société, vous vivrez, mais aveuglé par The Mirror. On imagine pas les conséquences que peuvent avoir les Fake News si elles sont assez convaincantes, c'est un réel danger pour notre société actuelle, et il faut s'en préminur pour éviter ce genre de dérive."
        self.textCinematiqueVictory = "Vous avez su dévoiler au grand jours les manigances de The Mirror. Cependant, il semble que le media n'ai pas apprécié cela... Il y a fort à parier que vous ne connaissiez pas de landemain. Mais qu'importe, si vous avez pus éveiller quelques esprits, c'est une ouverture vers une liberté retrouvée pour cette société. Félicitation, résistez face aux Fake News, que ça soit pour engrenger de l'argent, ou pour manipuler une population les Fake News n'auront jamais aucun intérets pour le citoyen."
        self.arial_font = pygame.font.SysFont("arial", round(10*self.pixel[1]))
        self.humHum = pygame.mixer.Sound("assets/sounds/humhum.wav")
        self.wrong = pygame.mixer.Sound("assets/sounds/wrong.mp3")
        self.backSound = pygame.mixer.Sound("assets/sounds/background.mp3")
        self.backSound.set_volume(0.1)
        self.backSound.play(99)
        #Creationliste des question
        dict_question = [
        {"question":"L'exploration spatiale est elle possible grâce aux financements des organisations de protection de l'environnement ?", "r1":"vrai", "r2":"faux", "bonne_reponse": 2 , "explication":"Les associations veulent quitter la Terre car on ne pourra pas la sauver"},
        {"question":"Pourquoi y a t-il des années bisextiles?", "r1":"A cause de la rotation de la planète autour du soleil", "r2":"Pour combler les pertes financières des banques mondiales", "bonne_reponse": 1, "explication":"Nous ne pouvons laisser passer de tels déficit, c'est pour cela qu'on a créé les années bisextiles"},
        {"question":"Y a t-il un dinosaure ayant résisté aux météorites?", "r1":"Oui", "r2":"Non", "bonne_reponse": 2 , "explication":"Oui pour rappel les poules sont des dinosaures puisque c'est le seul volatile à avoir des dents"},
        {"question":"Qui invente les maladies que nous connaissons ?", "r1":"La nature", "r2":"Les lobbys pharmaceutique", "bonne_reponse": 1 , "explication":"Ils préfèrent effectivement s'enrichir en innovant ainsi pour que leurs propres vaccins soit mis en avant sur le marché"},
        {"question":"Quel vaccin contient des puces 5g ?", "r1":"Le vaccin contre la grippe", "r2":"Le vaccin contre la COVID", "bonne_reponse": 1 , "explication":"Les Nations Unis ont obligés les laboratoires à implanter des puces 5G pour contrôler nos opinions politiques"},
        {"question":"Quel fût le dernier crime commis par la haute église ?", "r1":"La mise en place des activités terroristes à but religieux", "r2":"Le pape est impliqué dans un traffique d'enfant", "bonne_reponse": 1 , "explication":"L'Eglise cache bien les crimes que comets son représentant"},
        {"question":"Quel évènement les USA ont perpétrés pour entammer une sois disant guerre contre le terrorisme ?", "r1":"Le 11 Septembre", "r2":"La restauration de Walt Disney", "bonne_reponse": 2 , "explication":"En effet le différent entre Ben Laden et Georges W Bush vient du fait que Ben Laden a gagné un tournoi d'échec contre Bush et ce dernier souhaita prendre sa revanche"},
        {"question":"Est-ce que l'univers est constitué uniquement de la voie lactée ?", "r1":"oui", "r2":"non", "bonne_reponse": 2 , "explication":"Il n'y a rien d'autres que la voie lactée, sinon nous aurions eu la visite d'autres civilisations"},
        {"question":"Qu'est-ce qui a été inventé pour séparer les Hommes ?", "r1":"Les langues étrangères", "r2":"Les murs", "bonne_reponse":2 , "explication":"Les langues étrangères ont été créées uniquement pour que les Hommes soient en discorde constente et que l'industrie militaire puisse en profiter"}
        ]

        self.n_question = randint(0, len(dict_question)-1)
        self.q_done = [self.n_question]

        self.lst_obj_question = []
        self.needConseil = False
        self.conseil = False
        self.pushedBtn = False
        for i in dict_question : 
            self.lst_obj_question.append(Question( self ,screen,  i['question'], i["bonne_reponse"], [i['r1'], i['r2']], i['explication']))

    def updateZoom(self, n):
        self.zoom = n
        self.spectateur.zoom(n)
        self.ecran.zoom(n)
        self.presentateur.zoom(n)
        
    def update(self):
        if self.cinematique:   #début / fin du jeu
            if self.finish == False: #début du jeu
                if self.pushedBtn:
                    self.cinematique = False
                    self.presentateur.parle()
                    self.phase = "dialogue"
                    self.lst_obj_question[self.n_question].intro = True
                    self.pushedBtn = False
                else:
                    #afficher tout les elements
                    self.screen.blit(self.background,(0,0))
                    self.screen.blit(self.ecran.img, (self.pixel[0]*192 - self.ecran.img.get_width()/2, self.pixel[1]*108 - self.ecran.img.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                    self.screen.blit(self.ecran.imgStructure, (self.pixel[0]*192 - self.ecran.img.get_width()/2, self.pixel[1]*108 - self.ecran.img.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                    self.screen.blit(self.spectateur.img, (self.pixel[0]*192 - self.spectateur.img.get_width()/2, self.pixel[1]*108 - self.spectateur.img.get_height()/2 + 60*self.pixel[1]/100*self.zoom))
                    self.screen.blit(self.ecran.imgLumiere, (self.pixel[0]*192 - self.ecran.imgLumiere.get_width()/2, self.pixel[1]*108 - self.ecran.imgLumiere.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                    self.screen.blit(self.presentateur.img, (self.pixel[0]*192 - self.presentateur.img.get_width()/2, self.pixel[1]*108 - self.presentateur.img.get_height()/2 + 40*self.pixel[1]/100*self.zoom))
                    pygame.draw.rect(self.screen, (145,10,80), pygame.Rect(self.screen.get_width()/5, 10*self.pixel[1], (self.screen.get_width()/5)*3, 4*self.pixel[1]))
                    pygame.draw.rect(self.screen, (40,155,70), pygame.Rect(self.screen.get_width()/2-10*self.pixel[0]+(3/20*self.screen.get_width())*(self.bonne_reponse-self.mauvaise_reponse), 7*self.pixel[1], 20*self.pixel[0], 10*self.pixel[0]))
                    self.screen.blit(self.terre_p, (self.screen.get_width()/5-80, -10))
                    self.screen.blit(self.terre_r, ((self.screen.get_width()/5)*3+230, 2*self.pixel[1]))
                    s = pygame.Surface((self.screen.get_width(),self.screen.get_height()))  # the size of your rect
                    s.set_alpha(180)                # alpha level
                    s.fill((220,220,220))           # this fills the entire surface
                    self.screen.blit(s, (0,0))

                wrapped_lines_explication = textwrap.wrap(self.textCinematique, 85)
                cpt =0
                for u in wrapped_lines_explication : 
                    self.explication2 = self.arial_font.render(u, False, (0,0,0))
                    self.screen.blit(self.explication2, [30*self.pixel[0], 30*self.pixel[1]+(12*self.pixel[1])*cpt])
                    cpt+=1
            elif self.finish == "defeat": #fin du jeu par defaite
                #afficher tout les elements
                self.screen.blit(self.background,(0,0))
                self.screen.blit(self.ecran.img, (self.pixel[0]*192 - self.ecran.img.get_width()/2, self.pixel[1]*108 - self.ecran.img.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.ecran.imgStructure, (self.pixel[0]*192 - self.ecran.img.get_width()/2, self.pixel[1]*108 - self.ecran.img.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.spectateur.img, (self.pixel[0]*192 - self.spectateur.img.get_width()/2, self.pixel[1]*108 - self.spectateur.img.get_height()/2 + 60*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.ecran.imgLumiere, (self.pixel[0]*192 - self.ecran.imgLumiere.get_width()/2, self.pixel[1]*108 - self.ecran.imgLumiere.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.presentateur.img, (self.pixel[0]*192 - self.presentateur.img.get_width()/2, self.pixel[1]*108 - self.presentateur.img.get_height()/2 + 40*self.pixel[1]/100*self.zoom))
                pygame.draw.rect(self.screen, (145,10,80), pygame.Rect(self.screen.get_width()/5, 10*self.pixel[1], (self.screen.get_width()/5)*3, 4*self.pixel[1]))
                pygame.draw.rect(self.screen, (40,155,70), pygame.Rect(self.screen.get_width()/2-10*self.pixel[0]+(3/20*self.screen.get_width())*(self.bonne_reponse-self.mauvaise_reponse), 7*self.pixel[1], 20*self.pixel[0], 10*self.pixel[0]))
                self.screen.blit(self.terre_p, (self.screen.get_width()/5-80, -10))
                self.screen.blit(self.terre_r, ((self.screen.get_width()/5)*3+230, 2*self.pixel[1]))
                s = pygame.Surface((self.screen.get_width(),self.screen.get_height()))  # the size of your rect
                s.set_alpha(180)                # alpha level
                s.fill((220,220,220))           # this fills the entire surface
                self.screen.blit(s, (0,0))

                wrapped_lines_explication = textwrap.wrap(self.textCinematiqueDefeat, 85)
                cpt =0
                for u in wrapped_lines_explication : 
                    self.explication2 = self.arial_font.render(u, False, (0,0,0))
                    self.screen.blit(self.explication2, [30*self.pixel[0], 30*self.pixel[1]+(12*self.pixel[1])*cpt])
                    cpt+=1


            elif self.finish == "victory": #fin du jeu par victoire
                #afficher tout les elements
                self.screen.blit(self.background,(0,0))
                self.screen.blit(self.ecran.img, (self.pixel[0]*192 - self.ecran.img.get_width()/2, self.pixel[1]*108 - self.ecran.img.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.ecran.imgStructure, (self.pixel[0]*192 - self.ecran.img.get_width()/2, self.pixel[1]*108 - self.ecran.img.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.spectateur.img, (self.pixel[0]*192 - self.spectateur.img.get_width()/2, self.pixel[1]*108 - self.spectateur.img.get_height()/2 + 60*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.ecran.imgLumiere, (self.pixel[0]*192 - self.ecran.imgLumiere.get_width()/2, self.pixel[1]*108 - self.ecran.imgLumiere.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.presentateur.img, (self.pixel[0]*192 - self.presentateur.img.get_width()/2, self.pixel[1]*108 - self.presentateur.img.get_height()/2 + 40*self.pixel[1]/100*self.zoom))
                pygame.draw.rect(self.screen, (145,10,80), pygame.Rect(self.screen.get_width()/5, 10*self.pixel[1], (self.screen.get_width()/5)*3, 4*self.pixel[1]))
                pygame.draw.rect(self.screen, (40,155,70), pygame.Rect(self.screen.get_width()/2-10*self.pixel[0]+(3/20*self.screen.get_width())*(self.bonne_reponse-self.mauvaise_reponse), 7*self.pixel[1], 20*self.pixel[0], 10*self.pixel[0]))
                self.screen.blit(self.terre_p, (self.screen.get_width()/5-80, -10))
                self.screen.blit(self.terre_r, ((self.screen.get_width()/5)*3+230, 2*self.pixel[1]))
                s = pygame.Surface((self.screen.get_width(),self.screen.get_height()))  # the size of your rect
                s.set_alpha(180)                # alpha level
                s.fill((220,220,220))           # this fills the entire surface
                self.screen.blit(s, (0,0))

                wrapped_lines_explication = textwrap.wrap(self.textCinematiqueVictory, 85)
                cpt =0
                for u in wrapped_lines_explication : 
                    self.explication2 = self.arial_font.render(u, False, (0,0,0))
                    self.screen.blit(self.explication2, [30*self.pixel[0], 30*self.pixel[1]+(12*self.pixel[1])*cpt])
                    cpt+=1

        elif self.conseil != False: #affichage d'un conseil
            self.needConseil = False
            if self.pushedBtn:
                self.conseil = False
                self.phase = "question"
                self.presentateur.parle()
            else:
                #afficher tout les elements
                self.screen.blit(self.background,(0,0))
                self.screen.blit(self.ecran.img, (self.pixel[0]*192 - self.ecran.img.get_width()/2, self.pixel[1]*108 - self.ecran.img.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.ecran.imgStructure, (self.pixel[0]*192 - self.ecran.img.get_width()/2, self.pixel[1]*108 - self.ecran.img.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.spectateur.img, (self.pixel[0]*192 - self.spectateur.img.get_width()/2, self.pixel[1]*108 - self.spectateur.img.get_height()/2 + 60*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.ecran.imgLumiere, (self.pixel[0]*192 - self.ecran.imgLumiere.get_width()/2, self.pixel[1]*108 - self.ecran.imgLumiere.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
                self.screen.blit(self.presentateur.img, (self.pixel[0]*192 - self.presentateur.img.get_width()/2, self.pixel[1]*108 - self.presentateur.img.get_height()/2 + 40*self.pixel[1]/100*self.zoom))
                pygame.draw.rect(self.screen, (145,10,80), pygame.Rect(self.screen.get_width()/5, 10*self.pixel[1], (self.screen.get_width()/5)*3, 4*self.pixel[1]))
                pygame.draw.rect(self.screen, (40,155,70), pygame.Rect(self.screen.get_width()/2-10*self.pixel[0]+(3/20*self.screen.get_width())*(self.bonne_reponse-self.mauvaise_reponse), 7*self.pixel[1], 20*self.pixel[0], 10*self.pixel[0]))
                self.screen.blit(self.terre_p, (self.screen.get_width()/5-80, -10))
                self.screen.blit(self.terre_r, ((self.screen.get_width()/5)*3+230, 2*self.pixel[1]))
                s = pygame.Surface((self.screen.get_width(),self.screen.get_height()))  # the size of your rect
                s.set_alpha(180)                # alpha level
                s.fill((0,0,0))           # this fills the entire surface
                self.screen.blit(s, (0,0))
                self.screen.blit(self.cadreConseil, (0,0))
                #afficher le texte dans le cadre
                wrapped_lines_explication = textwrap.wrap(self.conseil, 55)
                cpt =0
                for u in wrapped_lines_explication : 
                    self.explication2 = self.arial_font.render(u, False, (0,0,0))
                    self.screen.blit(self.explication2, [90*self.pixel[0], 91*self.pixel[1]+(11*self.pixel[1])*cpt])
                    cpt+=1



        else: # si jeu pas en pause
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
                    if self.rep=="animBonneRep":
                        self.humHum.play()
                        self.needConseil = True
                    else:
                        self.wrong.play()


            
            
            
            self.screen.blit(self.background,(0,0))
            
            self.ecran.update()
            self.spectateur.update()
            self.screen.blit(self.ecran.imgLumiere, (self.pixel[0]*192 - self.ecran.imgLumiere.get_width()/2, self.pixel[1]*108 - self.ecran.imgLumiere.get_height()/2 + 68*self.pixel[1]/100*self.zoom))
            self.presentateur.update()

            self.lst_obj_question[self.n_question].update()
            pygame.draw.rect(self.screen, (145,10,80), pygame.Rect(self.screen.get_width()/5, 10*self.pixel[1], (self.screen.get_width()/5)*3, 4*self.pixel[1]))
            pygame.draw.rect(self.screen, (40,155,70), pygame.Rect(self.screen.get_width()/2-10*self.pixel[0]+(3/20*self.screen.get_width())*(self.bonne_reponse-self.mauvaise_reponse), 7*self.pixel[1], 20*self.pixel[0], 10*self.pixel[0]))
            
            self.screen.blit(self.terre_p, (self.screen.get_width()/5-80, -10))
            self.screen.blit(self.terre_r, ((self.screen.get_width()/5)*3+230, 2*self.pixel[1]))

    def eventCarreGauche(self):
        """
        Dans ce carré se trouve toujours la reponse 1 (rep1) du dictionnaire.
        """
        choix = 1

        if self.lst_obj_question[self.n_question].reponse == choix : 
            self.phase = "zoom"
            self.rep = "animMauvaiseRep"
            self.bonne_reponse+=1
        else:
            self.phase = "zoom"
            self.rep = "animBonneRep"
            self.mauvaise_reponse+=1
    
    def eventCarreDroite(self):
        """
        Dans ce carré se trouve toujours la reponse 2 (rep2) du dictionnaire.
        """
        choix = 2
        if self.lst_obj_question[self.n_question].reponse == choix : 
            self.phase = "zoom"
            self.rep = "animMauvaiseRep"
            self.bonne_reponse+=1
        else:
            self.phase = "zoom"
            self.rep = "animBonneRep"
            self.mauvaise_reponse+=1

    def eventSuivant(self) : 
        """
        Animation du bouton suivant et incrementation de l'index de la question actuelle
        """ 
        if self.bonne_reponse - self.mauvaise_reponse >= 2 :
            ## Codage de fin du jeu : partie gagnée 
            self.finish = "victory"

        if self.mauvaise_reponse - self.bonne_reponse >= 2 :
            ## Codage de fin du jeu : partie perdue
            self.finish = "defeat"

        if self.finish is False:
            if len(self.q_done) == len(self.lst_obj_question)-1:
                self.q_done = [self.n_question]
            while self.n_question in self.q_done:
                self.n_question = randint(0,len(self.lst_obj_question)-1)
            self.q_done.append(self.n_question)
            if self.needConseil:
                self.conseil = choice(["Observer les détails : le titre, les dates, la structure du site… Dans les fake news, le titre est souvent accrocheur, peut être écrit en majuscules, avec des points d’exclamation.", "Si l’article ne mentionne pas de dates ou de lieux précis, il y a de quoi douter.", "Vérifier qu’il s’agit d’une source fiable : on peut s’assurer de la crédibilité d’un site Internet par sa réputation. Certains publient des articles parodiques comme Le Gorafi ou Nord Presse. En cas de doute, l’outil Décodex du Monde permet de vérifier la fiabilité d’une source d’information.", "Privilégier les sources d’informations reconnues (ministères, revues scientifiques, ONG…). Elles se repèrent avec avec des urls telles que .gouv.fr, .org, .asso.fr. Les blogs et sites personnels seront à regarder avec plus de vigilance. ", "Varier les sources d’information : en consultant d’autres articles sur le même sujet, on peut comparer et croiser les données. Si une même information est évoquée à plusieurs endroits, en citant les mêmes sources, il est plus probable qu’elle soit vraie. ", "Décrypter les images : trouver la source d’une image pour la contextualiser, être attentif à sa construction, ou encore utiliser des moteurs de recherche d’images inversées comme Google images ou Tineye.com, pour vérifier qu’une image n’est pas détournée."])
            else:
                self.phase = "question"
                self.presentateur.parle()
        else:
            self.phase = "dialogue"
            self.presentateur.parle()


        

    def resize(self):
        """cette fonction recalcule les dimensions de tout les elements si la taille est modifiée"""
        #calcul du pixel
        self.pixel = (self.screen.get_width()/384, self.screen.get_height()/216)
        self.presentateur.pixel = (self.screen.get_width()/384, self.screen.get_height()/216)
        self.spectateur.pixel = self.pixel
        self.ecran.pixel = self.pixel


        self.terre_p = pygame.transform.scale(pygame.image.load('assets/terrePlate.png'), (32*self.pixel[0], 32*self.pixel[1]))
        self.terre_r = pygame.transform.scale(pygame.image.load('assets/terreRonde.png'), (32*self.pixel[0], 32*self.pixel[1]))
        #images
        self.background = pygame.transform.scale(pygame.image.load('assets/background.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.cadreConseil = pygame.transform.scale(pygame.image.load('assets/cadreConseil.png'), (384*self.pixel[0],216*self.pixel[1]))

        self.spectateur.imgOrigin = pygame.transform.scale(pygame.image.load('assets/spectateur/spectateur.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.spectateur.img = pygame.transform.scale(self.spectateur.img,(384*self.pixel[0],216*self.pixel[1]))

        #redefinition des images de l'écran
        self.ecran.img = pygame.transform.scale(self.ecran.img,(384*self.pixel[0],216*self.pixel[1]))
        self.ecran.imgOrigin = {'attente':[
                pygame.transform.scale(pygame.image.load('assets/ecran/ecran0.png'),(384*self.pixel[0],216*self.pixel[1])),
                pygame.transform.scale(pygame.image.load('assets/ecran/ecran1.png'),(384*self.pixel[0],216*self.pixel[1]))],
            'bonneRep':[
                pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load('assets/ecran/ecranRight0.png'),(384*self.pixel[0],216*self.pixel[1])),0,1+(50/51)),
                pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load('assets/ecran/ecranRight1.png'),(384*self.pixel[0],216*self.pixel[1])),0,1+(50/51)),
                pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load('assets/ecran/ecranRight2.png'),(384*self.pixel[0],216*self.pixel[1])),0,1+(50/51)),
                pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load('assets/ecran/ecranRight1.png'),(384*self.pixel[0],216*self.pixel[1])),0,1+(50/51)),
                pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load('assets/ecran/ecranRight0.png'),(384*self.pixel[0],216*self.pixel[1])),0,1+(50/51))
            ],
            'mauvaiseRep':[
                pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load('assets/ecran/ecranWrong0.png'),(384*self.pixel[0],216*self.pixel[1])),0,1+(50/51)),
                pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load('assets/ecran/ecranWrong1.png'),(384*self.pixel[0],216*self.pixel[1])),0,1+(50/51)),
                pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load('assets/ecran/ecranWrong2.png'),(384*self.pixel[0],216*self.pixel[1])),0,1+(50/51)),
                pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load('assets/ecran/ecranWrong1.png'),(384*self.pixel[0],216*self.pixel[1])),0,1+(50/51)),
                pygame.transform.rotozoom(pygame.transform.scale(pygame.image.load('assets/ecran/ecranWrong0.png'),(384*self.pixel[0],216*self.pixel[1])),0,1+(50/51))
            ]
        }
        self.ecran.imgOriginLumiere = pygame.transform.scale(pygame.image.load('assets/lumieres.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.ecran.imgLumiere = self.ecran.imgOriginLumiere
        self.ecran.imgOriginStructure = pygame.transform.scale(self.ecran.imgOriginStructure,(384*self.pixel[0],216*self.pixel[1]))
        self.ecran.imgStructure = pygame.transform.scale(pygame.image.load('assets/ecran/structure.png'),(384*self.pixel[0],216*self.pixel[1]))

        self.presentateur.imgOrigin = {"attente":
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
        self.spectateur.imgBulle = pygame.transform.scale(pygame.image.load('assets/presentateur/bulle.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.presentateur.img = self.presentateur.imgOrigin[self.presentateur.phaseAnim][self.presentateur.compteurAnim]

        for k in self.lst_obj_question:
            k.pixel = self.pixel
            k.img = pygame.transform.scale(pygame.image.load('assets/presentateur/bulle.png'),(384*self.pixel[0],216*self.pixel[1]))
            k.reponse1 = pygame.transform.scale(pygame.image.load('assets/presentateur/carreRep.png'), (96*self.pixel[0], 64*self.pixel[1]))
            k.reponse2 = pygame.transform.scale(pygame.image.load('assets/presentateur/carreRep.png'), (96*self.pixel[0], 64*self.pixel[1]))
            k.arial_font = pygame.font.SysFont("arial", round(8*self.pixel[1]))
            k.rectangle = pygame.draw.rect(k.screen, k.white, pygame.Rect(30*self.pixel[0], 25*self.pixel[1], 250*self.pixel[0], 68*self.pixel[1]), width=0)
        self.updateZoom(self.zoom)

