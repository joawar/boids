from moving_object import Moving_Object
from config import *
from vector import Vector2D
import pygame

class Boid(Moving_Object):
    def __init__(self, screen, pos, velocity):
        super().__init__(screen, pos, velocity, WHITE)
        self.boid_group.add(self)
        self.image = BOID_IMAGE.convert_alpha()
        self.image = self.original_image = pygame.transform.scale(self.image, (BOID_WIDTH, BOID_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.max_speed = BOID_MAX_SPEED
        
    def update(self, obstacle_list):
        super().update(obstacle_list)

    def cohesion(self): # based on pseudocode from kfish.org/boids/pseudocode.html
        """Returns a velcoity that makes the boids flocks towards a common center
        """
        perceived_centre = Vector2D(0,0)
        nearby_boid_count = 0
        boid_list = self.boid_group.sprites()
        for boid in boid_list:
            distance = (boid.pos - self.pos).length()
            if boid != self and distance < SIGHT_RADIUS:
                perceived_centre += boid.pos
                nearby_boid_count += 1
        try:
            perceived_centre = perceived_centre / nearby_boid_count
        except ZeroDivisionError:
            return Vector2D(0,0)
        return (perceived_centre - self.pos) * COHESION_POWER

    def alignment(self): # based on pseudocode from kfish.org/boids/pseudocode.html
        """Returns a velocity that makes the boids have a common velocity
        """
        perceived_velocity = Vector2D(0,0)
        nearby_boid_count = 0
        boid_list = self.boid_group.sprites()
        for boid in boid_list:
            distance = (boid.pos - self.pos).length()
            if boid != self and distance < SIGHT_RADIUS:
                perceived_velocity += boid.velocity
                nearby_boid_count += 1
        try:
            perceived_velocity = perceived_velocity / nearby_boid_count
        except ZeroDivisionError:
            return Vector2D(0,0)
        return (perceived_velocity - self.velocity) * ALIGNMENT_POWER
    
    def set_velocity(self, obstacle_list): 
        self.velocity += self.cohesion()
        self.velocity += self.alignment()
        super().set_velocity(obstacle_list)
    
    def separation(self): 
        """Returns a velocity that makes the boids not crash into each other
        """
        c = Vector2D(0,0) 
        boid_list = self.boid_group.sprites()
        for boid in boid_list:
            if boid != self:
                if (boid.pos - self.pos).length() < SIGHT_RADIUS/2:
                    c -= boid.pos - self.pos
        return c * SEPARATION_POWER