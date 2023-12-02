import pygame

NEIGHBOR_OFFSETS = [(i, j) for i in range(-4, 4) for j in range(-5, 5)]
PHYSICS_TILES = {"grass"}


class Tilemap:
    def __init__(self, screen, tile_size=16):
        self.tile_size = tile_size
        self.tilemap = {}  # блоки фиксированного размера на фиксированной сетке
        self.offgrid_tiles = []  # спрайты, свободно расположенные на карте
        self.screen = screen

        for i in range(100):
            self.tilemap[str(4+i) + ";10"] = {'type': 'grass', 'variant': 1, "pos": (4+i, 10)}

        for i in range(3):
            self.tilemap[str(10+i) + ";9"] = {'type': 'grass', 'variant': 1, "pos": (10+i, 9)}
            self.tilemap[str(13+i) + ";6"] = {'type': 'grass', 'variant': 1, "pos": (13+i, 6)}

        for i in range(3):
            self.tilemap[str(17+i) + ";3"] = {'type': 'grass', 'variant': 1, "pos": (17+i, 3)}

        for i in range(5):
            self.tilemap["3;" + str(7+i)] = {'type': 'grass', 'variant': 1, "pos": (3, 7+i)}

    """Функция tiles_around находит блоки в радиусе 5 блоков от pos (позиция существа)"""

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    """Функция physics_rects_around в радиусе 5 блоков от pos создает объекты класса Rect,
    с которыми сможет взаимодействовать существо."""

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(
                    tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surface, assets, camera_offset=(0, 0)):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surface.blit(assets[tile['type']][tile['variant']], (tile['pos'][0] *
                                                                 self.tile_size - camera_offset[0], tile['pos'][1] * self.tile_size - camera_offset[1]))
        for tile in self.offgrid_tiles:
            surface.blit()(assets[tile['type']][tile['variant']],
                           (tile['pos'][0] - camera_offset[0], tile['pos'][1] - camera_offset[1]))
