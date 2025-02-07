import pygame, sys
pygame.init()

from simulator.simulation import *
from physics.entity import *

screen = pygame.display.set_mode((640, 480))

s = Simulation(1, 1, True)
s.set_state(True)

while s.get_state():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s.set_state(False)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            for e in s.get_entities().values():
                if 
    
    s.update()
    
    screen.fill((0, 0, 0))
    s.display_on(screen)
    
    pygame.display.update()

pygame.quit()
