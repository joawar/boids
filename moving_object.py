from vector import Vector2D
from vector import intersect_circles
from config import *
from visible_object import Visible_Object
import pygame

class Moving_Object(Visible_Object):
    moving_object_group = pygame.sprite.Group()
    hoik_group = pygame.sprite.Group()
    boid_group = pygame.sprite.Group()
    def __init__(self, screen, pos, velocity, color):
        super().__init__(pos)
        self.velocity = velocity
        self.color = color
        self.screen = screen
        self.radius = HIT_RADIUS
        self.moving_object_group.add(self)
        self.acceleration = Vector2D(0,0)
    
    def update(self, obstacle_list):
        self.set_velocity(obstacle_list)
        self.move()
        rotation_angle = self.velocity.angle_to(self.reference_direction)
        self.rotate_image(rotation_angle)
            
    def limit_velocity(self, max_speed):
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize() * max_speed

    def accelerate(self):
        self.velocity += self.acceleration
        self.limit_velocity()

    def crash(self):
        if self.pos.x >= SCREEN_WIDTH or self.pos.x <= 0:
            self.kill()
        if self.pos.y >= SCREEN_HEIGHT or self.pos.y <= 0:
            self.kill()

    def move(self):
        self.pos += self.velocity
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
    def avoid_border(self):
        """Returns a velocity which will turn the moving object away from the border
        """
        width, height = SCREEN_RES
        ret = Vector2D(0,0)
        if self.pos.x > width - width * BORDER_SCREEN_RATIO:
            ret += Vector2D(-WALL_POWER, 0)
        if self.pos.x < width * BORDER_SCREEN_RATIO:
            ret += Vector2D(WALL_POWER, 0)
        if self.pos.y > height - height * BORDER_SCREEN_RATIO:
            ret += Vector2D(0, -WALL_POWER)
        if self.pos.y < height * BORDER_SCREEN_RATIO:
            ret += Vector2D(0, WALL_POWER)
        return ret
    
    def avoid_obstacle(self, obstacle_list):
        c = Vector2D(0,0)
        for obstacle in obstacle_list:
            if (self.pos - obstacle.pos).length() < SIGHT_RADIUS + obstacle.size:
                c -= (obstacle.pos - self.pos).normalize()
        return c * AVOID_OBSTACLE_POWER
    
    def set_velocity(self, obstacle_list):
        self.velocity += self.avoid_border()
        self.velocity += self.avoid_obstacle(obstacle_list)
        self.velocity += self.separation()
        self.limit_velocity(self.max_speed)