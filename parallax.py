import pygame


class BackgroundLayer: #Задний Фон
    def __init__(self, image_path, speed):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.speed = speed

    def draw(self, screen, player_pos):
        offset = player_pos[0] // self.speed % self.rect.width
        screen.blit(self.image, (offset - self.rect.width, 0))
        screen.blit(self.image, (offset, 0))

    def update(self, player_pos):
        pass  # не нужно обновлять позицию фона


class MiddleLayer:
    def __init__(self, image_path, speed):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.offset = 0

    def draw(self, screen, player_pos):
        offset = player_pos[0] // self.speed % self.rect.width
        screen.blit(self.image, (self.offset - self.rect.width, 0))
        screen.blit(self.image, (self.offset, 0))

    def update(self, player_pos):
        self.offset = player_pos[0] // self.speed % self.rect.width


class ForegroundLayer:
    def __init__(self, image_path, speed):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.offset = 0

    def draw(self, screen, player_pos):
        offset = player_pos[0] // self.speed % self.rect.width
        screen.blit(self.image, (self.offset - self.rect.width, 0))
        screen.blit(self.image, (self.offset, 0))

    def update(self, player_pos):
        self.offset = player_pos[0] // self.speed % self.rect.width