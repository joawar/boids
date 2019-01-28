from precode2 import *
from config import *

class Moving_Object():
    moving_object_list = []
    hoik_list = []
    boid_list = []
    def __init__(self, screen, pos, velocity, color):
        self.pos = pos
        self.velocity = velocity
        self.color = color
        self.screen = screen
        self.radius = HIT_RADIUS
        self.moving_object_list.append(self)

    def check_hit(self, obj):
        try:
            intersect_circles(self.pos, self.radius, obj.pos, obj.radius)
        except: 
            return False
        return True

    def crash(self, obstacle_list):
        for obstacle in obstacle_list:
            if self.check_hit(obstacle):
                self.die()

    def move(self):
        self.pos += self.velocity
    
    def follow_cursor(self, cursor_x, cursor_y):
        direction_vector_x = cursor_x - self.pos.x
        direction_vector_y = cursor_y - self.pos.y
        direction_vector = Vector2D(direction_vector_x, direction_vector_y)
        if abs(direction_vector) > 1:
            unit_vector = direction_vector/abs(direction_vector) # a unit vector pointing in the direction of the cursor
            self.velocity = unit_vector * abs(self.velocity)
    
    def draw(self):
        point1 = self.pos
        point2 = self.pos + self.velocity.normalized().rotate(180 + OI_ANGLE)*OI_SIZE
        point3 = self.pos + self.velocity.normalized().rotate(180 - OI_ANGLE)*OI_SIZE
        pygame.draw.polygon(self.screen, self.color, [[point1.x, point1.y], [point2.x, point2.y], [point3.x, point3.y]])

    def avoid_border(self):
        width, height = SCREEN_RES
        if self.pos.x > width - width * BORDER_SCREEN_RATIO and self.velocity.x > -TURN_BACK_SPEED:
            self.velocity = self.velocity.rotate(ROTATE_AWAY_FROM_BORDER_POWER)
        if self.pos.x < width * BORDER_SCREEN_RATIO and self.velocity.x < TURN_BACK_SPEED:
            self.velocity = self.velocity.rotate(ROTATE_AWAY_FROM_BORDER_POWER)
        if self.pos.y > height - height * BORDER_SCREEN_RATIO and self.velocity.y > -TURN_BACK_SPEED:
            self.velocity = self.velocity.rotate(ROTATE_AWAY_FROM_BORDER_POWER)
        if self.pos.y < height * BORDER_SCREEN_RATIO and self.velocity.y < TURN_BACK_SPEED:
            self.velocity = self.velocity.rotate(ROTATE_AWAY_FROM_BORDER_POWER)
    
    def avoid_obstacle(self, obstacle_list):
        c = Vector2D(0,0)
        for obstacle in obstacle_list:
            if abs(self.pos - obstacle.pos) < SIGHT_RADIUS:
                c -= obstacle.pos - self.pos
        return c * AVOID_OBSTACLE_POWER

    def set_new_velocity(self):
        raise Exception("Not implemented yet")
    
    def die(self):
        raise Exception("Not implemented yet")
    
    def separation(self):
        raise Exception("Not implemented yet")
    
    def eat(self):
        raise Exception("Not implemented yet")