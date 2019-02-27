import pygame
from vector import Vector2D

class Visible_Object(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.reference_direction = Vector2D(0,-1)


    def rotate_image(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)