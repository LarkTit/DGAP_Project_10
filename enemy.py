import pygame
from util import birds, skeletons, score
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
        self.is_damaging = False
        self.attack_delay = 0
        self.attack_time = 0
        self.reaction_time = 0
        self.attack_reaction = 0
        self.is_hit = 0
        self.lives = 3
        self.immune = False
        self.fade_time = 0

    def update(self, tilemap, assets, player):
        super().update(tilemap, assets)
        if self.is_moving and not self.is_attacking and self.lives > 0:
            self.flip = self.is_moving - 1
            if self.collisions['down']:
                self.set_action(assets, 'walk')
        elif self.collisions['down'] and not self.is_attacking and self.lives > 0:
            self.set_action(assets, 'idle')

        if self.is_attacking:
            if self.attack_time > 66:
                self.attack_time = 0
                self.is_attacking = False
                self.is_damaging = False
                self.speed = 1
                self.attack_delay = 1
            if self.attack_time > 15:
                self.is_damaging = True
            self.attack_time += 1

        if self.attack_delay:
            self.attack_delay += 1
            if self.attack_delay > 40:
                self.attack_delay = 0

        if self.is_hit:
            self.is_hit += 1
            if self.is_hit > 23 and self.lives > 0:
                self.immune = False
                self.is_hit = 0
                self.set_action(assets, "idle")

    def attack(self, assets):
        if not self.is_attacking and not self.attack_delay and self.lives > 0:
            self.attack_delay = 0
            self.is_attacking = True
            self.speed = 0
            self.set_action(assets, 'attack')

    def find_player(self, player):
        self.reaction_time += 1
        if self.reaction_time >= 27:
            self.reaction_time = 0
            surround_rect = pygame.Rect(self.pos[0] - 150, -150 + self.pos[1] + self.size[1], self.pos[0] + self.size[0] + 250, 150)
            if surround_rect.colliderect(player.rect()) and self.lives > 0:
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

    def hit_check(self, player, assets):
        if not self.immune and player.is_attacking and self.rect().colliderect(player.attack_rect()):
            self.is_hit = 1
            self.immune = True
            self.lives -= 1
            self.set_action(assets, 'hit')

    def attack_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]).move(15 + 15*self.flip, 0)

    def attack_check(self, player, assets):
        if not player.immune and self.is_damaging and self.attack_rect().colliderect(player.rect()) and self.lives > 0:
            player.is_hit = 1
            player.immune = True
            player.lives -= 1

    def explode(self, assets):
        self.set_action(assets, 'death')
        self.is_moving = 0
        self.is_dead = True
        if self.fade_time >= 50:
            if self in skeletons:
                skeletons.remove(self)
        self.fade_time += 1


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
        self.lives = 1
        self.is_hit = 0
        self.immune = False
        self.fade_time = 0

    def update(self, tilemap, assets, player):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        if self.aggressive and self.lives > 0:
            self.pos[0] += (-self.pos[0] + player.pos[0])/55
            self.pos[1] += (-self.pos[1] + player.pos[1])/55

        if self.pos[0] > player.pos[0]:
            self.flip = 1
        if self.pos[0] < player.pos[0]:
            self.flip = 0

        if self.is_hit:
            self.is_hit += 1
            if self.is_hit > 23:
                self.immune = False
                self.is_hit = 0
                self.set_action(assets, "fly")

        self.animation.update()

    def find_player(self, player):
        self.reaction_time += 1
        if self.reaction_time >= 24:
            self.reaction_time = 0
            surround_rect = pygame.Rect(self.pos[0] - 150, -150 + self.pos[1] + self.size[1], self.pos[0] + self.size[0] + 250, 300)
            if surround_rect.colliderect(player.rect()):
                self.aggressive = True

    def hit_check(self, player, assets):
        if not self.immune and player.is_attacking and self.rect().colliderect(player.attack_rect()):
            self.is_hit = 1
            self.immune = True
            self.lives -= 1
            self.set_action(assets, 'hit')

    def attack_check(self, player, assets):
        if not player.immune and self.rect().colliderect(player.rect()) and self.lives > 0:
            player.is_hit = 1
            player.immune = True
            player.lives -= 1

    def explode(self, assets):
        self.set_action(assets, 'death')
        self.is_dead = True
        if self.fade_time >= 20:
            if self in birds:
                birds.remove(self)
        self.fade_time += 1
