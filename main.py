import pygame
import tilemap
from random import choice
from player import Player
import entity
from parallax import BackgroundLayer, MiddleLayer, ForegroundLayer
from enemy import Skeleton, Bird
from util import load_image, load_images, load_map, Animation, TILESET, ENEMYPOS, load_tileset, load_tiles

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((640, 480))

"""
display - главный экран, на нём происходит рендер в низком разрешении.
Первый аргумент устанавливает длину с учётом соотношения сторон
"""
display = pygame.Surface((240 * screen.get_size()[0] // screen.get_size()[1], 240))

heart = pygame.image.load('assets\\heart.bmp').convert_alpha()

score = 0
birds = []
skeletons = []

"""Место хранения всех картинок и анимаций в виде словаря"""

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
    'player/hit': Animation(load_images('player/hit'), img_dur=7),

    'skeleton/idle': Animation(load_images('skeleton/idle'), img_dur=14),
    'skeleton/walk': Animation(load_images('skeleton/walk'), img_dur=6),
    'skeleton/hit': Animation(load_images('skeleton/hit'), img_dur=6),
    'skeleton/attack': Animation(load_images('skeleton/attack'), img_dur=4),
    'skeleton/death': Animation(load_images('skeleton/death'), img_dur=6),

    'bird/fly': Animation(load_images('bird/fly'), img_dur=6),
    'bird/hit': Animation(load_images('bird/hit'), img_dur=10),
    'bird/death': Animation(load_images('bird/death'), img_dur=5),
}

load_tileset('blue_bg')
load_tileset('blue_stone')
load_tileset('red_bg')
load_tileset('red_stone')
load_tileset('green_bg')
load_tileset('green_stone')

"""Инициализация объекта, отображающего игровой уровень."""

tilemap = tilemap.Tilemap(display)
tilemap.tilemap = load_map('tilemap0.csv')

for pos in ENEMYPOS:
    rand = choice((1, 2))
    if rand == 1:
        skeletons.append(Skeleton(display, pos))
        skeletons[-1].set_action(assets, 'idle')
    else:
        birds.append(Bird(display, pos))
        birds[-1].set_action(assets, 'fly')

"""Создание объекта игрока с начальной позицией (80,50)."""

player = Player(display, (80, 50))

""" Установка начального действия на игрока"""

player.set_action(assets, 'idle')

"""Список картинок и ссылок к ним для параллакса."""

backgrounds = [BackgroundLayer('assets/parallaxforestpack/parallax-mountain-bg.png', display),
               MiddleLayer('assets/parallaxforestpack/parallax-mountain-mountains.png', display),
               ForegroundLayer('assets/parallaxforestpack/parallax-mountain-foreground-trees.png', display, move_y_axis=True, y_position=50)
               ]

"""текст"""
pygame.font.init()
text = "SCORE: 0"
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 120)


"""Инициализация переменной, отвечающей за прокрутку камеры по горизонтали и вертикали"""
camera_scroll = [0, 0]


finished = False
""""Запуск игрового цикла. Обновления отображения, прокрутка камеры. Отображение всех изменений и управление частотой с помощью clock.tick(60)"""
while not finished:
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

    for skeleton in skeletons:
        skeleton.update(tilemap, assets, player)
        skeleton.render(display, camera_offset=render_scroll)
        skeleton.find_player(player)
        skeleton.attack_area(player, assets)
        skeleton.hit_check(player, assets)
        skeleton.attack_check(player, assets)
        if skeleton.lives <= 0 and skeleton in skeletons:
            skeletons.remove(skeleton)
            score += 1

    tilemap.render(display, assets, camera_offset=render_scroll)

    for bird in birds:
        bird.update(tilemap, assets, player)
        bird.render(display, camera_offset=render_scroll)
        bird.hit_check(player, assets)
        bird.find_player(player)
        bird.attack_check(player, assets)
        if bird.lives <= 0 and bird in birds:
            birds.remove(bird)
            score += 1
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

    for i in range(player.lives):
        display.blit(heart, (display.get_width() - 80 + 9*i, 12))

    text = "SCORE: " + str(score)
    img = font.render(text, True, (255, 255, 255))

    if player.lives <= 0:
        gameover_text = big_font.render("GAME OVER", True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(gameover_text, (screen.get_width() // 2 - 80, screen.get_height() // 2 + 10))

        pygame.display.update()
        pygame.time.delay(4000)
        finished = True

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    screen.blit(img, (screen.get_width() - 210, 95))
    pygame.display.update()
    clock.tick(60)

""""Очистка Pygame и выход из игры при завершении игрового цикла."""

pygame.quit()
