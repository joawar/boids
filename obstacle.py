from config import *
from vector import Vector2D
import pygame
from visible_object import Visible_Object

class Obstacle(Visible_Object):
    obstacle_group = pygame.sprite.Group()
    def __init__(self, pos, size):
        super().__init__(pos)
        self.size = self.width = self.height = size
        self.image = OBSTACLE_IMAGE.convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.obstacle_group.add(self)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y