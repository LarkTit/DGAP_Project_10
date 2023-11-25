import pygame
import os


def load_image(path):
    img = pygame.image.load("assets/" + path).convert_alpha()
    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir("assets/" + path)):
        images.append(load_image(path + '/' + img_name))
    return images
