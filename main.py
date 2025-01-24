import pygame, sys, random

from physics.entity import Entity
from geometry.vector import Vector
from geometry.shape import Circle
from geometry.utils import norm, squared_distance

pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

dt = 1/30 # en secondes
entities = [Entity(Vector(320, 240), Vector(0, 0), Circle(Vector(0, 0), 30), 1000000, color = (255, 255, 0))]

add = lambda: entities.append(Entity(Vector(random.uniform(1, 640), random.uniform(1, 480)), Vector(random.uniform(1, 50), random.uniform(1, 50)), Circle(Vector(0, 0), 10), 10000, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                add()
                print(len(entities))
    
    for cercle in entities:
        c = cercle.position
        for other in entities:
            if squared_distance(cercle.position, other.position) > 3:
                unitaire = other.position-c
                unitaire = unitaire*(cercle.mass*other.mass/norm(unitaire)**3)

                cercle.apply_force(unitaire)

        cercle.update(dt)

        center = (c[0], c[1])
        pygame.draw.circle(screen, cercle.color, center, cercle.collision_box.get_radius())
    
    pygame.display.update()
    clock.tick(30)