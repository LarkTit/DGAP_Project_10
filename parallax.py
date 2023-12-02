import pygame


class BackgroundLayer:  # Задний Фон
    def __init__(self, image_path, display, speed=0):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, display.get_size())
        self.rect = self.image.get_rect()
        self.speed = speed

    def draw(self, screen, camera_offset):
        offset = 0
        screen.blit(self.image, (offset - self.rect.width, 0))
        screen.blit(self.image, (offset, 0))


class MiddleLayer:
    def __init__(self, image_path, display, speed=1.5):
        self.display = display
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, display.get_size())
        self.rect = self.image.get_rect()
        self.speed = speed
        self.offset = 0

    def update(self, camera_offset):
        self.offset = -camera_offset[0] * self.speed // 10 % self.rect.width

    def draw(self, screen, camera_offset):
        self.update(camera_offset)
        self.display.blit(self.image, (self.offset - self.rect.width, 0))
        self.display.blit(self.image, (self.offset, 0))


class ForegroundLayer:
    def __init__(self, image_path, display, speed=6):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, display.get_size())
        self.rect = self.image.get_rect()
        self.speed = speed
        self.offset = 0

    def update(self, camera_offset):
        self.offset = -camera_offset[0] * self.speed // 10 % self.rect.width

    def draw(self, screen, camera_offset):
        self.update(camera_offset)
        screen.blit(self.image, (self.offset - self.rect.width, 0))
        screen.blit(self.image, (self.offset, 0))
