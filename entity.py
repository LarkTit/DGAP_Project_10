import pygame

"""PhysicsEntity - база для каждого существа, включая игрока"""
"""Физика, столкновения и прочее"""


class PhysicsEntity:
    def __init__(self, screen, pos):
        self.pos = list(pos)
        self.screen = screen
        self.size = (20, 50)
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def draw(self, camera_offset=(0, 0)):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(
            self.pos[0] - camera_offset[0], self.pos[1] - camera_offset[1], self.size[0], self.size[1]))

    def update(self, tilemap):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = [self.velocity[0], self.velocity[1]]

        if pygame.key.get_pressed()[pygame.K_d]:
            frame_movement[0] += 3
        if pygame.key.get_pressed()[pygame.K_a]:
            frame_movement[0] += -3

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                    self.velocity[0] = 0
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                    self.velocity[0] = 0
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.velocity[1] = 0
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

#        if movement[0] > 0:
#            self.flip = False
#        if movement[0] < 0:
#            self.flip = True

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

      #  self.animation.update()
