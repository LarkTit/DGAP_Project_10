import pygame
from entity import PhysicsEntity


class Skeleton(PhysicsEntity):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        self.size = (13, 32)
        self.type = 'skeleton'
        self.action = 'idle'
        self.anim_offset = (-22, -17)
        self.speed = 1
        self.is_attacking = False
        self.attack_delay = 0
        self.attack_time = 0
        self.reaction_time = 0
        self.attack_reaction = 0

    def update(self, tilemap, assets, player):
        super().update(tilemap, assets)
        if self.is_moving and not self.is_attacking:
            self.flip = self.is_moving - 1
            if self.collisions['down']:
                self.set_action(assets, 'walk')
        elif self.collisions['down'] and not self.is_attacking:
            self.set_action(assets, 'idle')

        if self.is_attacking:
            if self.attack_time > 66:
                self.attack_time = 0
                self.is_attacking = False
                self.speed = 1
                self.attack_delay = 1
            if self.attack_time > 15:
                pass
            self.attack_time += 1

        if self.attack_delay:
            self.attack_delay += 1
            if self.attack_delay > 40:
                self.attack_delay = 0

    def attack(self, assets):
        if not self.is_attacking and not self.attack_delay:
            self.attack_delay = 0
            self.is_attacking = True
            self.speed = 0
            self.set_action(assets, 'attack')

    def find_player(self, player):
        self.reaction_time += 1
        if self.reaction_time >= 27:
            self.reaction_time = 0
            surround_rect = pygame.Rect(self.pos[0] - 150, -150 + self.pos[1] + self.size[1], self.pos[0] + self.size[0] + 250, 150)
            if surround_rect.colliderect(player.rect()):
                if self.pos[0] > player.pos[0]:
                    self.is_moving = -1
                if self.pos[0] < player.pos[0]:
                    self.is_moving = 1

    def attack_area(self, player, assets):
        self.attack_reaction += 1
        if self.attack_reaction >= 20:
            self.attack_reaction = 0
            surround_rect = pygame.Rect(self.pos[0] - 30, -50 + self.pos[1] + self.size[1], self.pos[0], 50)
            if surround_rect.colliderect(player.rect()):
                self.attack(assets)


class Bird(PhysicsEntity):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        self.size = (30, 35)
        self.type = 'bird'
        self.action = 'fly'
        self.anim_offset = (-22, -17)
        self.speed = 1.5
        self.is_attacking = False
        self.attack_delay = 0
        self.attack_time = 0
        self.reaction_time = 0
        self.attack_reaction = 0
        self.aggressive = False

    def update(self, tilemap, assets, player):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        if self.aggressive:
            self.pos[0] += (-self.pos[0] + player.pos[0])/55
            self.pos[1] += (-self.pos[1] + player.pos[1])/55

        if self.pos[0] > player.pos[0]:
            self.flip = 1
        if self.pos[0] < player.pos[0]:
            self.flip = 0

        self.animation.update()

    def find_player(self, player):
        self.reaction_time += 1
        if self.reaction_time >= 24:
            self.reaction_time = 0
            surround_rect = pygame.Rect(self.pos[0] - 150, -150 + self.pos[1] + self.size[1], self.pos[0] + self.size[0] + 250, 300)
            if surround_rect.colliderect(player.rect()):
                self.aggressive = True
