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
        self.is_rolling = False
        self.roll_time = 0
        self.roll_delay = 0
        self.block_controls = False
        self.speed = 3

    def update(self, tilemap, assets):
        super().update(tilemap, assets)
        if self.is_moving and not self.is_rolling:
            self.flip = self.is_moving - 1
            if self.collisions['down']:
                self.set_action(assets, 'run')
        elif self.collisions['down'] and not self.is_rolling:
            self.set_action(assets, 'idle')

        if self.collisions["down"]:
            self.jumps = 2
            if self.fall_time > 30:
                self.set_action(assets, 'land')
            self.fall_time = 0

        if not self.collisions["down"] and not self.is_rolling:
            if self.velocity[1] < 0:
                self.set_action(assets, 'jump_up')
            if self.velocity[1] == 0:
                self.set_action(assets, 'jump_still')
            if self.velocity[1] > 0:
                self.set_action(assets, 'jump_down')
                self.fall_time += 1

        if self.is_rolling:
            self.roll_time += 1
            if self.collisions["down"]:
                self.set_action(assets, 'roll')
            else:
                self.set_action(assets, 'airspin')
            if self.roll_time >= 43:
                self.is_rolling = False
                self.roll_time = 0
                self.speed = 3

        if self.roll_delay > 0:
            self.roll_delay -= 1

    def jump(self):
        if self.is_rolling:
            self.is_rolling = False
            self.speed = 3
            self.roll_time = 0
            self.velocity[0] = 1
        if self.jumps == 1:
            self.velocity[1] = -3
            self.jumps -= 1
        if self.air_time < 6 and self.jumps == 2:
            self.velocity[1] = -3
            self.jumps -= 1
        elif self.jumps == 2:
            self.velocity[1] = -3
            self.jumps = 0

    def roll(self, assets):
        if self.roll_delay == 0:
            self.is_rolling = True
            self.roll_delay = 90
            if self.collisions["down"]:
                self.speed = 1
                self.set_action(assets, 'roll')
                if self.flip:
                    self.velocity[0] = -5
                else:
                    self.velocity[0] = 5
            else:
                self.set_action(assets, 'airspin')
                self.speed = 1.5
                if self.flip:
                    self.velocity[0] = -2.5
                else:
                    self.velocity[0] = 2.5
