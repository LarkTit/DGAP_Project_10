import pygame

"""Класс BackgroundLayer представляет задний фон игровой сцены с эффектом параллакса. Он содержит методы для 
инициализации, отрисовки и обновления заднего фона.
"""
class BackgroundLayer:  # Задний Фон

    """Метод init() инициализирует задний фон, принимая путь к изображению, объект отображения (display) и скорость
    движения фона (по умолчанию равна 0). Он загружает изображение, масштабирует его до размеров отображения и
    устанавливает скорость фона."""
    def __init__(self, image_path, display, speed=0):
        self.display = display
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, display.get_size())
        self.rect = self.image.get_rect()
        self.speed = speed

    """Метод draw() отрисовывает задний фон на отображении с учетом смещения камеры."""
    def draw(self, camera_offset):
        offset = 0
        self.display.blit(self.image, (offset - self.rect.width, 0))
        self.display.blit(self.image, (offset, 0))

"""Класс MiddleLayer представляет средний фон игровой сцены с эффектом параллакса. Он содержит методы для инициализации,
 отрисовки и обновления среднего фона."""
class MiddleLayer:
    """ Метод init() инициализирует средний фон, принимая путь к изображению, объект отображения (display)
    и скорость движения фона (по умолчанию равна 1.5). Он также загружает изображение, масштабирует его до размеров
    отображения и устанавливает скорость фона. """
    def __init__(self, image_path, display, speed=1.5):
        self.display = display
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, display.get_size())
        self.rect = self.image.get_rect()
        self.speed = speed
        self.offset = 0

    """Метод update() обновляет смещение среднего фона в зависимости от смещения камеры."""
    def update(self, camera_offset):
        self.offset = -camera_offset[0] * self.speed // 10 % self.rect.width

    """Метод draw() отрисовывает средний фон на отображении с учетом смещения камеры."""
    def draw(self, camera_offset):
        self.update(camera_offset)
        self.display.blit(self.image, (self.offset - self.rect.width, 0))
        self.display.blit(self.image, (self.offset, 0))

""""Класс ForegroundLayer представляет передний план игровой сцены с эффектом параллакса. Он содержит методы для 
инициализации, отрисовки и обновления переднего плана."""
class ForegroundLayer:
    """Метод init() инициализирует передний план, принимая путь к изображению, объект отображения (display), скорость
    движения фона (по умолчанию равна 6)"""
    def __init__(self, image_path, display, speed=6, move_y_axis=False, y_position=0):
        self.display = display
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, display.get_size())
        self.rect = self.image.get_rect()
        self.speed = speed
        self.offset = [0, 0]
        self.move_y_axis = move_y_axis
        self.y_position = y_position

    """Метод update() обновляет смещение переднего плана в зависимости от смещения камеры."""
    def update(self, camera_offset):
        self.offset[0] = -camera_offset[0] * self.speed // 10 % self.rect.width
        if self.move_y_axis:
            self.offset[1] = -camera_offset[1] * self.speed // 10

    """Метод draw() отрисовывает передний план на отображении с учетом смещения камеры."""
    def draw(self, camera_offset):
        self.update(camera_offset)
        self.display.blit(self.image, (self.offset[0] - self.rect.width, self.y_position + self.offset[1]))
        self.display.blit(self.image, (self.offset[0], self.y_position + self.offset[1]))
