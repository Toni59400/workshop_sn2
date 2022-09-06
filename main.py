from classGame import * 


pygame.init()



# générer la fenêtre de notre jeu
pygame.display.set_caption("Idiocracy")
screen = pygame.display.set_mode((1280, 720))
jeu = True
game = Game(screen)
dict_question = [{"question": "« Les personnes entièrement vaccinées développent le syndrome d’immunodéficience acquise (sida) »", "r1" : "Vrai", "r2" : "Faux", "bonne_reponse" : 2, "explication" : "Cette FakeNews provient du site 'Le Grand Réveil', et elle aurait pour source : 'Les rapports officiels du gouvernement britanique'"},
                 {"question": "« Le vaccin contre le Covid-19 contiendrait des puces électroniques 5G, pour nous tracer et ficher ! »", "r1" : "Vrai", "r2": "Faux", "bonne_reponse" : 2, "explication" : " Cette FakeNews est relayer sur les reseaux, démentie par le CHU de Toulouse dans un tweet."}
                 ]

lst_obj_question = []

for i in dict_question : 
    lst_obj_question.append(Question(screen, i['question'], i["bonne_reponse"], [i['r1'], i['r2']], i['explication']))

print(lst_obj_question)

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