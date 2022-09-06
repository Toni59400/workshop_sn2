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