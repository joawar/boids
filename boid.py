from moving_object import Moving_Object
from precode2 import *
from config import *

class Boid(Moving_Object):
    def __init__(self, screen, pos, velocity):
        super().__init__(screen, pos, velocity, WHITE)
        self.boid_list.append(self)

    def cohesion(self): # based on pseudocode from kfish.org/boids/pseudocode.html
        perceived_centre = Vector2D(0,0)
        nearby_boid_count = 0
        for boid in self.boid_list:
            distance = abs(boid.pos - self.pos)
            if boid != self and distance < SIGHT_RADIUS:
                perceived_centre += boid.pos
                nearby_boid_count += 1
        try:
            perceived_centre = perceived_centre / nearby_boid_count
        except ZeroDivisionError:
            return Vector2D(0,0)
        return (perceived_centre - self.pos) * COHESION_POWER

    def alignment(self): # based on pseudocode from kfish.org/boids/pseudocode.html
        perceived_velocity = Vector2D(0,0)
        nearby_boid_count = 0
        for boid in self.boid_list:
            distance = abs(boid.pos - self.pos)
            if boid != self and distance < SIGHT_RADIUS:
                perceived_velocity += boid.velocity
                nearby_boid_count += 1
        try:
            perceived_velocity = perceived_velocity / nearby_boid_count
        except ZeroDivisionError:
            return Vector2D(0,0)
        return (perceived_velocity - self.velocity) * ALIGNMENT_POWER
    
    def set_new_velocity(self, obstacle_list): 
        cohesion_component = self.cohesion()
        separation_component = self.separation()
        alignment_component = self.alignment()
        self.avoid_border()
        avoid_obstacle_component = self.avoid_obstacle(obstacle_list)
        self.velocity += cohesion_component + alignment_component + separation_component + avoid_obstacle_component
        if abs(self.velocity) > BOID_MAX_SPEED:
            self.velocity = self.velocity.normalized() * BOID_MAX_SPEED

    def die(self):
        self.moving_object_list.remove(self)
        self.boid_list.remove(self)
    
    def separation(self): 
        c = Vector2D(0,0) 
        for boid in self.boid_list:
            if boid != self:
                if abs(boid.pos - self.pos) < SIGHT_RADIUS/2:
                    c -= boid.pos - self.pos
        return c * SEPARATION_POWER
    