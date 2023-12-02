import pygame


class BackgroundLayer:  # Задний Фон
    def __init__(self, image_path, display, speed=0):
        self.display = display
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, display.get_size())
        self.rect = self.image.get_rect()
        self.speed = speed

    def draw(self, camera_offset):
        offset = 0
        self.display.blit(self.image, (offset - self.rect.width, 0))
        self.display.blit(self.image, (offset, 0))


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

    def draw(self, camera_offset):
        self.update(camera_offset)
        self.display.blit(self.image, (self.offset - self.rect.width, 0))
        self.display.blit(self.image, (self.offset, 0))


class ForegroundLayer:
    def __init__(self, image_path, display, speed=6, move_y_axis=False, y_position=0):
        self.display = display
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, display.get_size())
        self.rect = self.image.get_rect()
        self.speed = speed
        self.offset = [0, 0]
        self.move_y_axis = move_y_axis
        self.y_position = y_position

    def update(self, camera_offset):
        self.offset[0] = -camera_offset[0] * self.speed // 10 % self.rect.width
        if self.move_y_axis:
            self.offset[1] = -camera_offset[1] * self.speed // 10

    def draw(self, camera_offset):
        self.update(camera_offset)
        self.display.blit(self.image, (self.offset[0] - self.rect.width, self.y_position + self.offset[1]))
        self.display.blit(self.image, (self.offset[0], self.y_position + self.offset[1]))
