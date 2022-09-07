import pygame
from classGame import Game

pygame.init()



# générer la fenêtre de notre jeu
pygame.display.set_caption("Idiocratie 2, Le jeu")
screen = pygame.display.set_mode((1280, 720))
#le jeu tourne en 384 x 216 pixels
jeu = True
game = Game(screen)


while jeu:
    pygame.display.flip()
    game.update()
    x,y = pygame.mouse.get_pos()
    if (x<(96+20)*game.pixel[0] and x>20*game.pixel[0]) and (y<(140+64)*game.pixel[1] and y>140*game.pixel[1]):
        print('dessus')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu = False
        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        
# charger notre jeu 
clock = pygame.time.Clock()
fps = 30
running = True