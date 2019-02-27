from moving_object import Moving_Object
from vector import Vector2D
from config import *

class Hoik(Moving_Object):
    def __init__(self, screen, pos, velocity):
        super().__init__(screen, pos, velocity, HOIK_COLOR)
        self.hoik_group.add(self)
        self.image = HOIK_IMAGE.convert_alpha()
        self.image = self.original_image = pygame.transform.scale(self.image, (HOIK_WIDTH, HOIK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self, obstacle_list):
        super().update(obstacle_list)

    def find_nearest_boid(self):
        nearest_boid_pos = Vector2D(0,0)
        best_proximity = 100000 # big number
        boid_list = self.boid_group.sprites()
        if len(boid_list) == 0:
            raise Exception()
        for boid in boid_list:
            proximity = (self.pos - boid.pos).length()
            if proximity < best_proximity:
                nearest_boid_pos = boid.pos
                best_proximity = proximity
        return nearest_boid_pos
    
    def set_velocity(self, obstacle_list):
        try:
            nearest_boid_pos = self.find_nearest_boid()
            self.velocity += (nearest_boid_pos - self.pos).normalize() * TOWARDS_PREY_POWER
        except:
            pass
        self.velocity += self.avoid_border()
        self.velocity += self.avoid_obstacle(obstacle_list)
        self.velocity += self.separation()
        self.limit_velocity(HOIK_MAX_SPEED)
    
    def separation(self): 
        c = Vector2D(0,0) 
        hoik_list = self.hoik_group.sprites()
        for hoik in hoik_list:
            if hoik != self:
                if (hoik.pos - self.pos).length() < SIGHT_RADIUS/2:
                    c -= hoik.pos - self.pos
        return c * SEPARATION_POWER