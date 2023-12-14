import pygame

NEIGHBOR_OFFSETS = [(i, j) for i in range(-4, 4) for j in range(-5, 5)]
PHYSICS_TILES = {"grass", "blue_stone", "green_stone", "red_stone"}


class Tilemap:
    def __init__(self, screen, tile_size=16):
        self.tile_size = tile_size
        self.tilemap = {}  # блоки фиксированного размера на фиксированной сетке
        self.offgrid_tiles = []  # спрайты, свободно расположенные на карте
        self.screen = screen

    """Функция tiles_around находит блоки в радиусе 5 блоков от pos (позиция существа)"""

    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
            matches[-1]['pos'] = matches[-1]['pos'].copy()
            matches[-1]['pos'][0] *= self.tile_size
            matches[-1]['pos'][1] *= self.tile_size
            if not keep:
                del self.tilemap[loc]
        return matches

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
            if tile['type'] in PHYSICS_TILES:
                surface.blit(assets[tile['type']][tile['variant']], (tile['pos'][0] *
                                                                     self.tile_size - camera_offset[0], tile['pos'][1] * self.tile_size - camera_offset[1]))

        for tile in self.offgrid_tiles:
            surface.blit()(assets[tile['type']][tile['variant']],
                           (tile['pos'][0] - camera_offset[0], tile['pos'][1] - camera_offset[1]))

    def render_bg(self, surface, assets, camera_offset=(0, 0)):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['type'] not in PHYSICS_TILES:
                surface.blit(assets[tile['type']][tile['variant']], (tile['pos'][0] *
                                                                     self.tile_size - camera_offset[0], tile['pos'][1] * self.tile_size - camera_offset[1]))
