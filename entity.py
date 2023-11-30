import pygame

"""PhysicsEntity - база для каждого существа, включая игрока"""
"""Физика, столкновения и прочее"""


class PhysicsEntity:
    def __init__(self, screen, pos):
        self.pos = list(pos)
        self.screen = screen
        self.size = (20, 40)
        self.velocity = [0, 0]
        self.is_moving = 0
        self.air_time = 0
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.flip = False

        self.type = ''
        self.action = ''
        self.animation = 0
        self.anim_offset = (-3, -3)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, assets, action):
        if action != self.action or not self.animation:
            self.action = action
            self.animation = assets[self.type + '/' + self.action].copy()

    def draw(self, camera_offset=(0, 0)):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(
            self.pos[0] - camera_offset[0], self.pos[1] - camera_offset[1], self.size[0], self.size[1]))

    def render(self, screen, camera_offset=(0, 0)):
        screen.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                    (self.pos[0] - camera_offset[0] + self.anim_offset[0], self.pos[1] - camera_offset[1] + self.anim_offset[1]))

    def update(self, tilemap, assets):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = [self.velocity[0], self.velocity[1]]

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

#        if movement[0] > 0:
#            self.flip = False
#        if movement[0] < 0:
#            self.flip = True

        self.velocity[1] = min(5, self.velocity[1] + 0.15)

        if self.collisions['down']:
            self.air_time = 0
        else:
            self.air_time += 1

        self.animation.update()
