import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))
finished = False

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            pygame.quit()

    pygame.display.update()
    clock.tick(60)
