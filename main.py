import pygame
import tilemap
from player import Player
import entity
from parallax import BackgroundLayer, MiddleLayer, ForegroundLayer
from util import load_image, load_images, load_map, Animation, TILESET, load_tileset, load_tiles

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((640, 480))

"""
display - главный экран, на нём происходит рендер в низком разрешении.
Первый аргумент устанавливает длину с учётом соотношения сторон
"""
display = pygame.Surface((240 * screen.get_size()[0] // screen.get_size()[1], 240))

assets = {
    "grass": load_tiles("tiles/grass"),
    "blue_bg": load_tiles("tiles/blue_bg"),
    "blue_stone": load_tiles("tiles/blue_stone"),
    "red_bg": load_tiles("tiles/red_bg"),
    "red_stone": load_tiles("tiles/red_stone"),
    "green_bg": load_tiles("tiles/green_bg"),
    "green_stone": load_tiles("tiles/green_stone"),
    'player/idle': Animation(load_images('player/idle'), img_dur=6),
    'player/run': Animation(load_images('player/run'), img_dur=5),
    'player/jump_up': Animation(load_images('player/jump_up')),
    'player/jump_still': Animation(load_images('player/jump_still')),
    'player/jump_down': Animation(load_images('player/jump_down')),
    'player/roll': Animation(load_images('player/roll'), img_dur=6),
    'player/airspin': Animation(load_images('player/airspin'), img_dur=7),
    'player/climb_low': Animation(load_images('player/climb_low'), img_dur=7),
    'player/climb_high': Animation(load_images('player/climb_high'), img_dur=7),
    'player/land': Animation(load_images('player/land'), loop=False),
}

load_tileset('blue_bg')
load_tileset('blue_stone')
load_tileset('red_bg')
load_tileset('red_stone')
load_tileset('green_bg')
load_tileset('green_stone')

tilemap = tilemap.Tilemap(display)
tilemap.tilemap = load_map('tilemap1.csv')

player = Player(display, (80, 50))
player.set_action(assets, 'idle')

backgrounds = [BackgroundLayer('assets/parallaxforestpack/parallax-mountain-bg.png', display),
               MiddleLayer('assets/parallaxforestpack/parallax-mountain-mountains.png', display),
               ForegroundLayer('assets/parallaxforestpack/parallax-mountain-foreground-trees.png', display, move_y_axis=True, y_position=15)
               ]

"""Камера"""
camera_scroll = [0, 0]

"""Частицы"""


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

    tilemap.render_bg(display, assets, camera_offset=render_scroll)

    for background in backgrounds:
        background.draw(render_scroll)

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
                # player.velocity[0] += 3
                player.is_moving += 1
            if event.key == pygame.K_a:
                # player.velocity[0] -= 3
                player.is_moving -= 1
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_LSHIFT:
                player.roll(assets)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.is_moving -= 1
                # player.velocity[0] -= 3
            if event.key == pygame.K_a:
                player.is_moving += 1
                # player.velocity[0] += 3

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
