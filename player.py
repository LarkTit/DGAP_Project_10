import pygame
from entity import PhysicsEntity


class Player(PhysicsEntity):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        self.size = (25, 31)
        self.type = 'player'
        self.action = 'idle'
        self.jumps = 2
        self.fall_time = 0
        self.anim_offset = (-10, -8)

    def update(self, tilemap, assets):
        super().update(tilemap, assets)
        if self.is_moving:
            self.flip = self.is_moving - 1
            if self.collisions['down']:
                self.set_action(assets, 'run')
        elif self.collisions['down']:
            self.set_action(assets, 'idle')

        if self.collisions["down"]:
            self.jumps = 2
            if self.fall_time > 30:
                self.set_action(assets, 'land')
            self.fall_time = 0

        if not self.collisions["down"]:
            if self.velocity[1] < 0:
                self.set_action(assets, 'jump_up')
            if self.velocity[1] == 0:
                self.set_action(assets, 'jump_still')
            if self.velocity[1] > 0:
                self.set_action(assets, 'jump_down')
                self.fall_time += 1

    def jump(self):
        if self.jumps == 1:
            self.velocity[1] = -3
            self.jumps -= 1
        if self.air_time < 6 and self.jumps == 2:
            self.velocity[1] = -3
            self.jumps -= 1
        elif self.jumps == 2:
            self.velocity[1] = -3
            self.jumps = 0
