import pygame, sys
pygame.init()

from simulator.simulation import *
from physics.entity import *
from geometry.utils import *

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

s = Simulation(1, 1, True)
s.set_state(True)

s.add_entity(Entity([Circle(Vector(320, 240), 50)], 10, Vector(0.01, 0.01)))

arrow = [False]*4 # right, left, up, down
while s.get_state():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s.set_state(False)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                arrow[0] = True
            if event.key == pygame.K_LEFT:
                arrow[1] = True
            if event.key == pygame.K_UP:
                arrow[2] = True
            if event.key == pygame.K_DOWN:
                arrow[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                arrow[0] = False
            if event.key == pygame.K_LEFT:
                arrow[1] = False
            if event.key == pygame.K_UP:
                arrow[2] = False
            if event.key == pygame.K_DOWN:
                arrow[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for key in s.get_entities():
                if Vector(*pygame.mouse.get_pos()) in s.get_entities()[key].get_body()[0]:
                    s.set_editing(True, key)
    
    camera_speed = 0.5
    if arrow[0]:
        s.moove_camera(camera_speed, 0)
    if arrow[1]:
        s.moove_camera(-camera_speed, 0)
    if arrow[2]:
        s.moove_camera(0, -camera_speed)
    if arrow[3]:
        s.moove_camera(0, camera_speed)

    screen.fill((0, 0, 0))

    s.update()
    s.display_on(screen)

    is_editing, id_ent = s.on_editing()
    if is_editing:
        center = s.get_entities()[id_ent].get_body()[0].get_center()
        grey = 3*norm(center)%256
        pygame.draw.rect(screen, (200, 200, 200), pygame.rect.Rect(0, 0, width//3, height))
    
    pygame.display.update()

pygame.quit()
