import pygame
pygame.init()

# générer la fenêtre de notre jeu
pygame.display.set_caption("WorkShop2023")
screen = pygame.display.set_mode((1280, 720))
jeu = True
game = GamePingpong(screen, 3)

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