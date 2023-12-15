import pygame

"""PhysicsEntity - база для каждого существа, включая игрока"""
"""Физика, столкновения и прочее"""


class PhysicsEntity:
    def __init__(self, screen, pos):
        self.pos = list(pos)
        self.screen = screen
        self.size = (19, 40)
        self.velocity = [0, 0]
        self.is_moving = 0
        self.air_time = 0
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.surround = {'up': [], 'down': [], 'right': [], 'left': []}
        self.flip = False
        self.speed = 0
        self.is_attacking = False
        self.attack_time = 0

        self.type = ''
        self.action = ''
        self.animation = 0
        self.anim_offset = (-3, -3)

    """Возвращает прямоугольник сущности"""

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    """"Проверяет есть ли у сущности анимация и устанавливает ее"""

    def set_action(self, assets, action):
        if action != self.action or not self.animation:
            self.action = action
            self.animation = assets[self.type + '/' + self.action].copy()

    """Вывод прямоугольника сущности на экран"""

    def draw(self, camera_offset=(0, 0)):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(
            self.pos[0] - camera_offset[0], self.pos[1] - camera_offset[1], self.size[0], self.size[1]))

    """Анимирует сущность на экране"""

    def render(self, screen, camera_offset=(0, 0)):
        screen.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                    (self.pos[0] - camera_offset[0] + self.anim_offset[0], self.pos[1] - camera_offset[1] + self.anim_offset[1]))

    """Проверяет окружение сущности на наличие стен"""

    def check_surroundings(self, tilemap, epsilon):
        self.surround = {'up': [], 'down': [], 'right': [], 'left': []}
        surround_rect = self.rect().inflate(epsilon[0], epsilon[1])
        for rect in tilemap.physics_rects_around(self.pos):
            if surround_rect.colliderect(rect):
                if surround_rect.right >= rect.left and surround_rect.centerx < rect.centerx - 8:
                    self.surround['right'].append(rect)
                if surround_rect.left <= rect.right and surround_rect.centerx > rect.centerx + 8:
                    self.surround['left'].append(rect)
                if surround_rect.top <= rect.bottom and surround_rect.centery > rect.centery:
                    self.surround['up'].append(rect)
                if surround_rect.bottom >= rect.top and surround_rect.centery < rect.centery:
                    self.surround['down'].append(rect)
        return self.surround

    """Обновляется позиция сущности на экране. Проверяется происходит ли столкновение со стенкой, если оно произошло, то позиция не меняется."""

    def update(self, tilemap, assets):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = [self.is_moving * self.speed + self.velocity[0], self.velocity[1]]

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                    frame_movement[0] = 0
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                    frame_movement[0] = 0
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.velocity[1] = 1
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                    self.velocity[1] = 0
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.15)
        if self.collisions['down']:
            if self.velocity[0] < 0:
                self.velocity[0] = min(0, self.velocity[0] + 0.1)
            else:
                self.velocity[0] = max(0, self.velocity[0] - 0.1)

        if self.collisions['down']:
            self.air_time = 0
        else:
            self.air_time += 1

        self.animation.update()
