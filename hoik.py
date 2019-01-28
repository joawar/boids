from moving_object import Moving_Object
from precode2 import *
from config import *

class Hoik(Moving_Object):
    def __init__(self, screen, pos, velocity):
        super().__init__(screen, pos, velocity, HOIK_COLOR)
        self.hoik_list.append(self)
    
    def eat(self):
        for boid in self.boid_list:
            if self.check_hit(boid):
                boid.die()
            
    def find_nearest_boid(self):
        nearest_boid_pos = Vector2D(DEFAULT_HOIK_X_POSITION, DEFAULT_HOIK_Y_POSITION)
        best_proximity = 100000 # big number
        for boid in self.boid_list:
            proximity = abs(self.pos - boid.pos)
            if proximity < best_proximity:
                nearest_boid_pos = boid.pos
                best_proximity = proximity
        return nearest_boid_pos
    
    def set_new_velocity(self, obstacle_list):
        nearest_boid_pos = self.find_nearest_boid()
        self.avoid_border()
        avoid_obstacle_component = self.avoid_obstacle(obstacle_list)
        towards_prey_component = (nearest_boid_pos - self.pos) * TOWARDS_PREY_POWER
        separation_component = self.separation()
        self.velocity += avoid_obstacle_component + towards_prey_component
        if abs(self.velocity) > HOIK_MAX_SPEED:
            self.velocity = self.velocity.normalized() * HOIK_MAX_SPEED
        
    def die(self):
        self.moving_object_list.remove(self)
        self.hoik_list.remove(self)
    
    def separation(self): 
        c = Vector2D(0,0) 
        for hoik in self.hoik_list:
            if hoik != self:
                if abs(hoik.pos - self.pos) < SIGHT_RADIUS/2:
                    c -= hoik.pos - self.pos
        return c * SEPARATION_POWER