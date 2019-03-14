from vector import intersect_circles
from vector import intersect_rectangle_circle
from config import *
from moving_object import Moving_Object
from hoik import Hoik
from boid import Boid
from obstacle import Obstacle
from math import acos, degrees
from vector import Vector2D
import pygame

pygame.init()
screen = pygame.display.set_mode(SCREEN_RES)
clock = pygame.time.Clock()
obstacle_list = [Obstacle(Vector2D(OBSTACLE_1_X, OBSTACLE_1_Y), OBSTACLE_1_SIZE), 
                 Obstacle(Vector2D(OBSTACLE_2_X, OBSTACLE_2_Y), OBSTACLE_2_SIZE)]

while True:    
    pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))
    clock.tick(30) # limit to 30FPS 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # spawn boids at left mouse click
            if event.button == 1: 
                spawn_x, spawn_y = pygame.mouse.get_pos()
                spawn_pos = Vector2D(spawn_x, spawn_y)
                spawn_velocity = Vector2D(START_VELOCITY_X, START_VELOCITY_Y)
                boid = Boid(screen, spawn_pos, spawn_velocity)
            # spawn hoiks at left mouse click
            if event.button == 3: 
                spawn_x, spawn_y = pygame.mouse.get_pos()
                spawn_pos = Vector2D(spawn_x, spawn_y)
                spawn_velocity = Vector2D(START_VELOCITY_X, START_VELOCITY_Y)
                hoik = Hoik(screen, spawn_pos, spawn_velocity)

    # collision testing, updating, and drawing
    pygame.sprite.groupcollide(Moving_Object.moving_object_group, Obstacle.obstacle_group, True, False)
    pygame.sprite.groupcollide(Moving_Object.boid_group, Moving_Object.hoik_group, True, False)
    Moving_Object.moving_object_group.update(Obstacle.obstacle_group.sprites())
    Moving_Object.moving_object_group.draw(screen)
    Obstacle.obstacle_group.draw(screen)

    pygame.display.update()