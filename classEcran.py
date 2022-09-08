import pygame

class Ecran:
    def __init__(self, game,screen, pixel):
        """Class des specateurs
        param : screen - pygame Object - l'écran sur lequel on affiche
                pixel - tuple - la dimension d'un pixel (largeur, hauteur)"""
        self.screen = screen
        self.game = game
        self.pixel = pixel
        self.zoomN = 0
        
        self.imgOriginLumiere = pygame.transform.scale(pygame.image.load('assets/lumieres.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.imgLumiere = self.imgOriginLumiere
        self.imgOrigin = {'attente':[
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
        self.animSpeed = 35
        self.compteurAnim = self.animSpeed
        self.compteurAnimAttente = 0
        self.img = self.imgOrigin["attente"][0]
        self.imgOriginStructure = pygame.transform.scale(pygame.image.load('assets/ecran/structure.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.imgStructure = self.imgOriginStructure

    def update(self):
        """cette fonction met à jour l'affichage et la position des spectateurs"""
        if self.game.phase == "animBonneRep":
            self.img = self.imgOrigin["bonneRep"][self.compteurAnim//8]
            self.compteurAnim -= 1
            if self.compteurAnim == 0:
                self.compteurAnim = self.animSpeed
                self.game.phase = "dezoom"
                self.img = self.imgOrigin["attente"][self.compteurAnimAttente]
                self.zoom(self.zoomN)
        
        elif self.game.phase == "animMauvaiseRep":
            self.img = self.imgOrigin["mauvaiseRep"][self.compteurAnim//8]
            self.compteurAnim -= 1
            if self.compteurAnim == 0:
                self.compteurAnim = self.animSpeed
                self.game.phase = "dezoom"
                self.img = self.imgOrigin["attente"][self.compteurAnimAttente]
                self.zoom(self.zoomN)
        
        elif self.game.compteur%10 == 0:
            self.compteurAnimAttente = int(not bool(self.compteurAnimAttente))

        self.screen.blit(self.img, (self.pixel[0]*192 - self.img.get_width()/2, self.pixel[1]*108 - self.img.get_height()/2 + 68*self.pixel[1]/100*self.game.zoom))
        self.screen.blit(self.imgStructure, (self.pixel[0]*192 - self.img.get_width()/2, self.pixel[1]*108 - self.img.get_height()/2 + 68*self.pixel[1]/100*self.game.zoom))

    def zoom(self, n):
        self.zoomN = n
        self.img = pygame.transform.rotozoom(self.imgOrigin['attente'][self.compteurAnimAttente],0,1+(n*(2.5/255)))
        self.imgStructure = pygame.transform.rotozoom(self.imgOriginStructure,0,1+(n*(2.5/255)))
        self.imgLumiere = pygame.transform.rotozoom(self.imgOriginLumiere,0,1+(n*(2.5/255)))