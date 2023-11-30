import pygame
import tilemap
from player import Player
from util import load_image, load_images, Animation

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

"""
display - главный экран, на нём происходит рендер в низком разрешении.
Первый аргумент устанавливает длину с учётом соотношения сторон
"""
display = pygame.Surface((240 * screen.get_size()[0] // screen.get_size()[1], 240))

assets = {
    "grass": load_images("tiles/grass"),
    "player": load_image("player/idle/idle1.bmp"),
    'player/idle': Animation(load_images('player/idle'), img_dur=6),
    'player/run': Animation(load_images('player/run'), img_dur=5),
    'player/jump_up': Animation(load_images('player/jump_up')),
    'player/jump_still': Animation(load_images('player/jump_still')),
    'player/jump_down': Animation(load_images('player/jump_down')),
    'player/land': Animation(load_images('player/land'), loop=False),
}

tilemap = tilemap.Tilemap(display)
player = Player(display, (80, 50))
player.set_action(assets, 'idle')

"""Камера"""
camera_scroll = [0, 0]

finished = False
while not finished:
    display.fill((112, 255, 255))

    camera_scroll[0] += (player.rect().centerx - display.get_width() // 2 - camera_scroll[0] + 15) / 20
    camera_scroll[1] += (player.rect().centery - display.get_height() // 2 - camera_scroll[1]) / 15
    if player.flip:
        camera_scroll[0] -= 3
    else:
        camera_scroll[0] += 2
    render_scroll = (int(camera_scroll[0]), int(camera_scroll[1]))

    # TODO
    # Нужно сделать два-три слоя для заднего фона для параллакса
    # (самый дальний фон статичен, второй немного двигается вместе с персонажем ну и так далее)

    player.update(tilemap, assets)
    player.render(display, camera_offset=render_scroll)

    tilemap.render(display, assets, camera_offset=render_scroll)
    # for rect in tilemap.physics_rects_around(player.pos):
    #     pygame.draw.rect(display, (0, 0, 0), rect.move(-render_scroll[0], -render_scroll[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.velocity[0] += 3
                player.is_moving += 1
            if event.key == pygame.K_a:
                player.velocity[0] -= 3
                player.is_moving -= 1
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_LSHIFT:
                player.dash()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.is_moving -= 1
                player.velocity[0] -= 3
            if event.key == pygame.K_a:
                player.is_moving += 1
                player.velocity[0] += 3

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
