from precode2 import *
from config import *

class Obstacle():
    def __init__(self, screen, pos, radius):
        self.pos = pos
        self.radius = radius
        self.screen = screen
    def draw(self):
        pygame.draw.circle(self.screen, GREEN, self.pos.as_point, self.radius)