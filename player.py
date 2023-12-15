import pygame
from entity import PhysicsEntity


class Player(PhysicsEntity):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        self.size = (18, 31)
        self.type = 'player'
        self.action = 'idle'
        self.jumps = 2
        self.fall_time = 0
        self.anim_offset = (-15, -8)
        self.is_rolling = False
        self.climb_time = 0
        self.is_climbing = 0
        self.roll_time = 0
        self.roll_delay = 0
        self.block_controls = False
        self.speed = 3
        self.no_interrupt = False
        self.climb_done = True
        self.climb_type = ''
        self.attack_type = 0
        self.attack_window = 0
        self.attack_buffer = 0
        self.lives = 7
        self.is_hit = 0
        self.immune = False

    def attack_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]).inflate(37, 0).move(15 + 6*self.flip, 0)

    def update(self, tilemap, assets):
        super().update(tilemap, assets)
        if self.is_moving and not self.no_interrupt:
            self.flip = self.is_moving - 1
            if self.collisions['down']:
                self.set_action(assets, 'run')
        elif self.collisions['down'] and not self.no_interrupt:
            self.set_action(assets, 'idle')

        if self.collisions["down"]:
            self.jumps = 2
            self.fall_time = 0

        if not self.collisions["down"] and not self.no_interrupt:
            if self.velocity[1] < -0.5:
                self.set_action(assets, 'jump_up')
            if abs(self.velocity[1]) < 0.5:
                self.set_action(assets, 'jump_still')
            if self.velocity[1] > 0.5:
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
                self.no_interrupt = False
                self.roll_time = 0
                self.speed = 3

        if self.roll_delay > 0:
            self.roll_delay -= 1

        self.is_climbing = False

        self.climb_update(assets, tilemap, 'right', 1)
        self.climb_update(assets, tilemap, 'left', -1)

        if self.is_climbing:
            self.speed = 1
        elif not self.climb_done:
            self.velocity[0] = 0
            self.anim_offset = (-15, -8)
            self.no_interrupt = False
            self.speed = 3
            self.climb_done = True

        if self.is_attacking:
            if self.attack_time > 20:
                self.attack_time = 0
                self.is_attacking = False
                self.no_interrupt = False
                self.speed = 3
                self.attack_window = 1
                self.set_action(assets, 'idle')
                self.anim_offset = (-15, -8)
            self.attack_time += 1

        if self.attack_window and self.attack_type:
            if self.attack_window > 26:
                self.attack_type = 0
                self.attack_window = 0
            self.attack_window += 1

        if not self.is_attacking and self.attack_buffer > 0:
            self.attack(assets)
            self.attack_buffer = 0

        if self.is_hit:
            self.is_hit += 1
            if self.is_hit > 27:
                self.immune = False
                self.is_hit = 0
                self.set_action(assets, "idle")

    def jump(self):
        if self.is_rolling:
            self.is_rolling = False
            self.no_interrupt = False
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

    def attack(self, assets):
        if not self.is_attacking and not self.no_interrupt:
            self.is_attacking = True
            self.no_interrupt = True
            self.anim_offset = (-20, -17)
            self.speed = 0.7
            if self.attack_type == 0:
                self.set_action(assets, 'attack1')
                self.attack_type = 1
            else:
                self.set_action(assets, 'attack2')
                self.attack_type = 0
        else:
            self.attack_buffer = 1

    def roll(self, assets):
        if self.roll_delay == 0 and not self.no_interrupt:
            self.is_rolling = True
            self.no_interrupt = True
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

    def climb_update(self, assets, tilemap, direction, flip):
        if len(self.check_surroundings(tilemap, (10, 35))["up"]) < 3 and not self.check_surroundings(tilemap, (-17, 40))["down"] and 0 < len(self.check_surroundings(tilemap, (5, 5))[direction]) <= 2 and self.collisions[direction]:
            tiles = sorted(self.check_surroundings(tilemap, (5, 5))[direction], key=lambda x: x.bottom)
            if self.climb_done:
                if tiles[0].bottom > self.rect().bottom:
                    self.climb_type = 'low'
                    self.pos[1] = tiles[0].top - 14
                else:
                    self.pos[1] = tiles[0].top - 2
                    self.climb_type = 'high'
            self.climb(assets, flip)

    def climb(self, assets, flip):
        self.is_climbing = True
        self.no_interrupt = True
        self.climb_done = False
        self.anim_offset = (-15 + flip * 3, -8)
        self.velocity[0] = flip * 1
        if self.climb_type == 'low':
            self.velocity[1] = -0.5
        else:
            self.velocity[1] = -1
        if self.climb_type == 'low':
            self.set_action(assets, 'climb_low')
        else:
            self.set_action(assets, 'climb_high')
