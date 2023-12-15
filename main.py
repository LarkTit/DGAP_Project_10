import pygame
import tilemap
from player import Player
import entity
from parallax import BackgroundLayer, MiddleLayer, ForegroundLayer
from enemy import Skeleton, Bird
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
    "green_stone": load_tiles("tiles/green_stone"),
    'player/attack1': Animation(load_images('player/attack1'), img_dur=5),
    'player/attack2': Animation(load_images('player/attack2'), img_dur=5),
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

    'skeleton/idle': Animation(load_images('skeleton/idle'), img_dur=14),
    'skeleton/walk': Animation(load_images('skeleton/walk'), img_dur=6),
    'skeleton/hit': Animation(load_images('skeleton/hit'), img_dur=6),
    'skeleton/attack': Animation(load_images('skeleton/attack'), img_dur=4),
    'skeleton/death': Animation(load_images('skeleton/death'), img_dur=6),

    'bird/fly': Animation(load_images('bird/fly'), img_dur=6),
    'bird/hit': Animation(load_images('bird/fly'), img_dur=10),
    'bird/death': Animation(load_images('bird/fly'), img_dur=5),
}

load_tileset('blue_bg')
load_tileset('blue_stone')
load_tileset('red_bg')
load_tileset('red_stone')
load_tileset('green_bg')
load_tileset('green_stone')

tilemap = tilemap.Tilemap(display)
tilemap.tilemap = load_map('maplevel2.csv')

player = Player(display, (110, 1400))
player.set_action(assets, 'idle')


backgrounds = [BackgroundLayer('assets/parallaxforestpack/parallax-mountain-bg.png', display),
               MiddleLayer('assets/parallaxforestpack/parallax-mountain-mountains.png', display),
               ForegroundLayer('assets/parallaxforestpack/parallax-mountain-foreground-trees.png', display, move_y_axis=True, y_position=15)
               ]

skeleton = Skeleton(display, (180, 50))
skeleton.set_action(assets, 'idle')

bird = Bird(display, (180, 50))
bird.set_action(assets, 'fly')


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

    for background in backgrounds:
        background.draw(render_scroll)

    tilemap.render_bg(display, assets, camera_offset=render_scroll)

    player.update(tilemap, assets)
    player.render(display, camera_offset=render_scroll)

    skeleton.update(tilemap, assets, player)
    skeleton.render(display, camera_offset=render_scroll)
    skeleton.find_player(player)
    skeleton.attack_area(player, assets)

    tilemap.render(display, assets, camera_offset=render_scroll)

    bird.update(tilemap, assets, player)
    bird.render(display, camera_offset=render_scroll)
    bird.find_player(player)
    # for rect in tilemap.physics_rects_around(player.pos):
    #     pygame.draw.rect(display, (0, 0, 0), rect.move(-render_scroll[0], -render_scroll[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.attack(assets)
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
