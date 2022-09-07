import pygame
from classGame import Game

pygame.init()



# générer la fenêtre de notre jeu
pygame.display.set_caption("Idiocratie 2, Le jeu")
screen = pygame.display.set_mode((1280,720), pygame.RESIZABLE)
#le jeu tourne en 384 x 216 pixels
jeu = True
game = Game(screen)
clock = pygame.time.Clock()
fps = 30

while jeu:
    clock.tick(fps)
    pygame.display.flip()
    game.update()
    x,y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            game.resize()
        #Bouton gauche
        if (x<(96+20)*game.pixel[0] and x>20*game.pixel[0]) and (y<(140+64)*game.pixel[1] and y>140*game.pixel[1]) and event.type == pygame.MOUSEBUTTONUP :
            game.eventCarreGauche()
        #Bouton droite
        if (x<(96+140)*game.pixel[0] and x>140*game.pixel[0]) and (y<(140+64)*game.pixel[1] and y>140*game.pixel[1]) and event.type == pygame.MOUSEBUTTONUP :
            game.eventCarreDroite()
        if event.type == pygame.QUIT:
            jeu = False
        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        

