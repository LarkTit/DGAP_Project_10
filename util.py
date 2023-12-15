import pygame
import os

TILESET = {}
ENEMYPOS = []
birds = []
skeletons = []
score = 0

"""Загружает изображение по указанному пути и возвращает его в формате pygame.Surface."""


def load_image(path):
    img = pygame.image.load("assets/" + path).convert_alpha()
    return img


"""Загружает все изображения по указанному пути и вовзвращает их в виде списка pygame.Surface"""


def load_images(path):
    images = []
    for img_name in sorted(os.listdir("assets/" + path)):
        images.append(load_image(path + '/' + img_name))
    return images


"""Загружает тайлы по указанному пути и возвращает их в виде словаря, где ключи - номер файла, а значения - изображения в нужном формате."""


def load_tiles(path):
    images = {}
    for img_name in sorted(os.listdir("assets/" + path)):
        images[int(img_name[:-4])] = load_image(path + '/' + img_name)
    return images


"""загружает тайлы, содержащиеся в указанной директории, и добавляет их в словарь TILESET, где ключами являются номера тайлов, а значениями - пути к соответствующим изображениям."""


def load_tileset(path):
    with open(path) as file:
        file.readline(3)
        tile_string = ''
        while "</tileset>" not in tile_string:
            tile_string = file.readline()
            tile_string.strip()
            split_string = list(tile_string.split(" \" "))
            tile_id = split_string[1]
            tile_name = split_string[3]
            TILESET["tile_id"] = tile_name
        file.close()


def load_tileset(path):
    for img_name in sorted(os.listdir("assets/tiles/" + path)):
        img_name = img_name[:-4]
        TILESET[img_name] = path


""" Загрузка карты игрового уровня по указанному пути и возвращает ее в виде словаря, где ключами являются координаты тайлов, а значениями - информация о типе, варианте и позиции тайлов.
"""


def load_map(path):
    y = 0
    x = 0
    tilemap = {}
    with open('assets/' + path) as file:
        while True:
            y += 1
            x = 0
            tiles_id = list(file.readline().strip().split(','))
            if not tiles_id or tiles_id[0] == '':
                break
            for tile_id in tiles_id:
                x += 1
                if tile_id == '0':
                    ENEMYPOS.append((x*16, y*16))
                tile_id = str(int(tile_id) + 1)
                if tile_id in TILESET:
                    tilemap[str(x)+';'+str(y)] = {'type': TILESET[tile_id], 'variant': int(tile_id), "pos": (x, y)}
    file.close()
    return tilemap


""" Анимация изображений. Содержит методы при инициализации, обновления и получения текущего изображения анимации."""


class Animation:
    def __init__(self, images, img_dur=6, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
