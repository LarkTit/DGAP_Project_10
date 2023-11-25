import pygame
import tilemap
import entity
from util import load_image, load_images

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
    "player": load_image("player/idle/idle1.bmp")
}

tilemap = tilemap.Tilemap(display)
player = entity.PhysicsEntity(display, (80, 50))

"""Камера"""
camera_scroll = [0, 0]

finished = False
while not finished:
    display.fill((112, 255, 255))

    camera_scroll[0] += (player.rect().centerx - display.get_width() // 2 - camera_scroll[0]) / 30
    camera_scroll[1] += (player.rect().centery - display.get_height() // 2 - camera_scroll[1]) / 30
    render_scroll = (int(camera_scroll[0]), int(camera_scroll[1]))

    # TODO
    # Нужно сделать два-три слоя для заднего фона для параллакса
    # (самый дальний фон статичен, второй немного двигается вместе с персонажем ну и так далее)

    player.update(tilemap)
    player.draw(camera_offset=render_scroll)

    tilemap.render(display, assets, camera_offset=render_scroll)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
