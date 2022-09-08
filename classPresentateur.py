import pygame
from random import randint
import textwrap

class Presentateur:
    def __init__(self, game,screen, pixel):
        """Class des specateurs
        param : screen - pygame Object - l'écran sur lequel on affiche
                pixel - tuple - la dimension d'un pixel (largeur, hauteur)"""
        self.screen = screen
        self.game = game
        self.timerParle = 0
        self.pixel = pixel
        self.arial_font = pygame.font.SysFont("arial", round(8*self.pixel[1]))
        self.phaseAnim = "attente"
        self.compteurAnim = 0
        self.phraseIntro = ["Bonjour cher monsieur c’est impressionnant que vous puissiez tenir debout après toutes ces années bloquées dans la glace ahahah","Pendant tout ce temps la société tel que vous la connaissiez n’existe plus, nous sommes tous plus développés intellectuellement grâce à la société d’information “the mirror” qui nous a ouvert les yeux sur ce qui se passait réellement dans ce monde corrompu ahaha","Saviez-vous qu’en réalité Michael Jackson n’était pas mort il avait juste encore changé d’apparence ahaha","Disons merci à “the mirror” !", "Nous allons maintenant vous faire passer un petit test pour savoir si vous êtes l’un des nôtres","j’espère que vous êtes prêt !"]  
        self.compteurIntro = 0
        self.phraseDefeat = ["Eh bien nous sommes heureux de vous dire que vous vous integrerez parfaitement de notre société ahahah !", "En effet vos tests sont concluants, c'est excellent bravo à vous !", "Vous êtes maintenant libre d'utiliser The Mirror pour tout connaitre de ce monde ahahah !"]
        self.compteurDefeat = 0
        self.phraseVictory = ["Hummm... Euh... Bien...", "Nous allons devoir écourter notre émission pour aujourd'hui ahahah...", "Il semble que vous soyez trop idiot pour comprendre la vérité, vous incarnez la corruption de notre ancienne société", "The mirror nous en a délivré, et personne ici ne souhaite que quelqu'un vienne nous influencer dans la mauvaise voie.", "En éspérant vous revoir bientôt ahahah !"]
        self.compteurVictory = 0
        #sons
        self.bling = pygame.mixer.Sound("assets/sounds/bling.mp3")
        self.voice = pygame.mixer.Sound("assets/sounds/voice.mp3")
        self.imgBulle = pygame.transform.scale(pygame.image.load('assets/presentateur/bulle.png'),(384*self.pixel[0],216*self.pixel[1]))
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
        print(self.game.phase)
        if self.phaseAnim=="attente":
            if self.game.compteur % 10 == 0:
                if randint(0,30) == 0 and self.game.phase not in ["zoom", "dezoom"]: #mettre l'animation miroir
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
                print(self.compteurAnim)
                print(len(self.imgOrigin[self.phaseAnim]))
                self.img = self.imgOrigin[self.phaseAnim][self.compteurAnim]
                self.zoom(self.game.zoom)
            self.timerParle -= 1
            if self.timerParle == 0:
                self.phaseAnim = "attente"
                self.compteurAnim = 0
        elif self.phaseAnim == "animation0":
            if self.game.compteur %3 == 0:
                if self.sensAnim == 1:
                    self.compteurAnim +=1
                    if self.compteurAnim == 4:
                        self.sensAnim = 0
                        self.bling.play()
                else:
                    self.compteurAnim -= 1
                    if self.compteurAnim == -1:
                        self.phaseAnim = "attente"
                        self.compteurAnim = 0
                self.img = self.imgOrigin[self.phaseAnim][self.compteurAnim]
                self.zoom(self.game.zoom)
        if self.game.phase == "dialogue":
            self.screen.blit(self.imgBulle,(0,0))
            if self.game.finish is False:
                wrapped_lines_rep1 = textwrap.wrap(self.phraseIntro[self.compteurIntro], 64)
                c=0
                for j in wrapped_lines_rep1:
                    self.rep1 = self.arial_font.render(j, False, (0,0,0))
                    self.screen.blit(self.rep1, (30*self.pixel[0], 25*self.pixel[1]+(10*self.pixel[1])*c))
                    c+=1
                if self.game.pushedBtn:
                    self.compteurIntro += 1
                    self.parle()
                    if self.compteurIntro == len(self.phraseIntro):
                        self.game.phase = 'question'
            elif self.game.finish == "defeat":
                wrapped_lines_rep1 = textwrap.wrap(self.phraseDefeat[self.compteurDefeat], 64)
                c=0
                for j in wrapped_lines_rep1:
                    self.rep1 = self.arial_font.render(j, False, (0,0,0))
                    self.screen.blit(self.rep1, (30*self.pixel[0], 25*self.pixel[1]+(10*self.pixel[1])*c))
                    c+=1
                if self.game.pushedBtn:
                    self.compteurDefeat += 1
                    self.parle()
                    if self.compteurDefeat == len(self.phraseDefeat):
                        self.game.phase = "cinematique"
                        self.game.cinematique = True
            elif self.game.finish == "victory":
                wrapped_lines_rep1 = textwrap.wrap(self.phraseVictory[self.compteurVictory], 64)
                c=0
                for j in wrapped_lines_rep1:
                    self.rep1 = self.arial_font.render(j, False, (0,0,0))
                    self.screen.blit(self.rep1, (30*self.pixel[0], 25*self.pixel[1]+(10*self.pixel[1])*c))
                    c+=1
                if self.game.pushedBtn:
                    self.compteurVictory += 1
                    self.parle()
                    if self.compteurVictory == len(self.phraseVictory):
                        self.game.phase = "cinematique"
                        self.game.cinematique = True

        self.screen.blit(self.img, (self.pixel[0]*192 - self.img.get_width()/2, self.pixel[1]*108 - self.img.get_height()/2 + 40*self.pixel[1]/100*self.game.zoom))
        
    def zoom(self, n):
        print(self.phaseAnim, self.compteurAnim)
        self.img = pygame.transform.rotozoom(self.imgOrigin[self.phaseAnim][self.compteurAnim],0,1+(n*(2.5/255)))
        if n > 50:
            self.img.set_alpha(255-(n-50)*12.75)

    def parle(self):
        self.voice.stop()
        self.voice.play()
        self.timerParle = 30
        self.phaseAnim = 'parle'