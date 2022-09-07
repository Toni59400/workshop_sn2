from tkinter import Label
import pygame
import textwrap

class Question():
    '''
    
    '''
    def __init__(self, game, screen, question, reponse, propositions, explication):
        self.white = (255,255,0)
        self.screen = screen 
        self.question = question #string
        self.reponse = reponse #index dans la liste proposition
        self.propositions = propositions #liste de propositions
        self.explication = explication #string
        self.game = game
        self.pixel = game.pixel
        self.img = pygame.transform.scale(pygame.image.load('assets/presentateur/bulle.png'),(384*self.pixel[0],216*self.pixel[1]))
        self.reponse1 = pygame.transform.scale(pygame.image.load('assets/presentateur/carreRep.png'), (96*self.pixel[0], 64*self.pixel[1]))
        self.reponse2 = pygame.transform.scale(pygame.image.load('assets/presentateur/carreRep.png'), (96*self.pixel[0], 64*self.pixel[1]))
        self.arial_font = pygame.font.SysFont("arial", round(8*self.pixel[1]))
        self.rectangle = pygame.draw.rect(self.screen, self.white, pygame.Rect(30*self.pixel[0], 25*self.pixel[1], 250*self.pixel[0], 68*self.pixel[1]), width=0)

    def update(self):
        """cette fonction met à jour l'affichage et la position des spectateurs"""
        if self.game.phase == "question" : 
            self.black = (0,0,0)
            self.screen.blit(self.img, (0,0))
            # prochaine ligne = rectangle avec les reponses affichées dedans 
            self.screen.blit(self.reponse1, (20*self.pixel[0], 140*self.pixel[1]))
            self.screen.blit(self.reponse1, (140*self.pixel[0], 140*self.pixel[1]))
            width_max = 64
            width_max_res = 23
            wrapped_lines_rep1 = textwrap.wrap(self.propositions[0], width_max_res)
            wrapped_lines_rep2 = textwrap.wrap(self.propositions[1], width_max_res)
            wrapped_lines = textwrap.wrap(self.question, width_max)
            c=0
            for i in wrapped_lines : 
                self.text_question = self.arial_font.render(i, False, self.black)
                self.screen.blit(self.text_question, [30*self.pixel[0], 25*self.pixel[1]+(10*self.pixel[1])*c])
                c+=1
            
            c=0
            for j in wrapped_lines_rep1:
                self.rep1 = self.arial_font.render(j, False, self.black)
                self.screen.blit(self.rep1, (25*self.pixel[0], 145*self.pixel[1]+(10*self.pixel[1])*c))
                c+=1

            c=0
            for k in wrapped_lines_rep2:
                self.rep2 = self.arial_font.render(k, False, self.black)
                self.screen.blit(self.rep2, (145*self.pixel[0], 145*self.pixel[1]+(10*self.pixel[1])*c))
                c+=1