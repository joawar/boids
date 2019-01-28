from precode2 import *
from config import *
from moving_object import Moving_Object
from hoik import Hoik
from boid import Boid
from obstacle import Obstacle
from math import acos, degrees


print("Left click to spawn boids, right click to spawn hoiks.")
pygame.init()
screen = pygame.display.set_mode(SCREEN_RES)
clock = pygame.time.Clock()
# boid_list = []
# hoik_list = []
# moving_object_list = []
obstacle_list = [Obstacle(screen, Vector2D(OBSTACLE_1_X, OBSTACLE_1_Y), OBSTACLE_1_SIZE), 
                 Obstacle(screen, Vector2D(OBSTACLE_2_X, OBSTACLE_2_Y), OBSTACLE_2_SIZE)]

while True:    
    pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))
    time_passed = clock.tick(30) # limit to 30FPS 
    time_passed_seconds = time_passed / 1000.0   # convert to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                spawn_x, spawn_y = pygame.mouse.get_pos()
                spawn_pos = Vector2D(spawn_x, spawn_y)
                spawn_velocity = Vector2D(START_VELOCITY_X, START_VELOCITY_Y)
                boid = Boid(screen, spawn_pos, spawn_velocity)
                boid_list = boid.boid_list
                moving_object_list = boid.moving_object_list
            if event.button == 3:
                spawn_x, spawn_y = pygame.mouse.get_pos()
                spawn_pos = Vector2D(spawn_x, spawn_y)
                spawn_velocity = Vector2D(START_VELOCITY_X, START_VELOCITY_Y)
                hoik = Hoik(screen, spawn_pos, spawn_velocity)
                moving_object_list = hoik.moving_object_list

    
    for moving_object in Moving_Object.moving_object_list:
        moving_object.set_new_velocity(obstacle_list)
        moving_object.move()
        moving_object.draw()
        moving_object.crash(obstacle_list)
        if type(moving_object) == Hoik:
            moving_object.eat()

    for obstacle in obstacle_list:
            obstacle.draw()
    

    pygame.display.update()