import pygame

"""Placeholder for every entity including player"""
"""Basic physics stuff here"""


class PhysicsEntity:
    def __init__(self, screen, pos):
        self.pos = list(pos)
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
