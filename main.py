# Pygame
import pygame
pygame.init()
pygame.font.init()

width, height = 1200, 700
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Newtonian Sandbox")

# GUI
from gui.interface import *
from gui import tick

# Simulator
from simulator.controls import *
mouse = Mouse()
keyboard = Keyboard()

from simulator.simulation import *
from physics.entity import *

clock = pygame.time.Clock()

simulations = [Simulation(24, 24, True)]
tablist.add("CACA")
simulations[0].add_entity(Entity(Vector(0, 0), Polygon([Vector(100, 150), Vector(150, 150), Vector(150, 100), Vector(100, 100)]), 0.1))
simulations[0].add_entity(Entity(Vector(0, 0), Polygon([Vector(0, 100), Vector(50, 50), Vector(0, 0)]), 0.1))
#simulations[0].add_entity(Entity(Vector(-10, 0), Circle(Vector(600, -200), 30), 0.1))
#simulations[0].add_entity(Entity(Vector(0, 0), Circle(Vector(350, -200), 30), 0.1))
key = -1

run = True
while run:
    screen.fill((0, 0, 0))

    keyboard.clear()
    mouse.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # updating controls
        mouse.update(event)
        keyboard.update(event)

        # updating gui
        update_toolbar_events(event)

    # updating GUI
    update_tablist_events(mouse)
    toolbar_manager.update(tick)

    # key events
    if keyboard.key_down("f11"):
        pygame.display.toggle_fullscreen()
    
    if keyboard.key_down("right"):
        if tablist.get_current() > -1:
            simulations[tablist.get_current()]._follow += 1
            simulations[tablist.get_current()]._follow %= len(simulations[tablist.get_current()].get_entities())
    
    if keyboard.key_down("up"):
        simulations[tablist.get_current()].zoom(0.1)
    
    if keyboard.key_down("down"):
        simulations[tablist.get_current()].zoom(-0.1)

    flip = lambda v: Vector(v[0], -v[1])

    if mouse.right_click():
        if mouse.right_click_down():
            entities = simulations[tablist.get_current()].get_entities()
            for k in entities:
                if flip(Vector(*mouse.get_position())) in entities[k].body:
                    key = k
                    simulations[tablist.get_current()].set_state(False)
                    break
        
            pygame.mouse.get_rel()
        elif key == -1:
            simulations[tablist.get_current()].move_camera(*pygame.mouse.get_rel())

    if mouse.left_click_down():
        flag = True
        for e in simulations[tablist.get_current()].get_entities().values():
            if e.body.get_center() == flip(Vector(*mouse.get_position())):
                flag = False
                break
        
        if flag:
            simulations[tablist.get_current()].add_entity(Entity(Vector(0, 0), Circle(flip(Vector(*mouse.get_position())), 30), 0.1))

    if pygame.mouse.get_just_released()[2] and key != -1:
        horizontal_flip = lambda v: Vector(-v[0], v[1])
        entities = simulations[tablist.get_current()].get_entities()
        entities[key].apply_force(horizontal_flip(Vector(*mouse.get_position())-flip(entities[key].body.get_center())))

        simulations[tablist.get_current()].set_state(True)
        key = -1

    # updating current tab
    if tablist.get_current() == -1:
        main_menu.update(mouse)
        screen.blit(main_menu.surface(), main_menu.get_position())
    else:
        simulations[tablist.get_current()].update()
        simulations[tablist.get_current()].display_on(screen)

        if key != -1:
            flip = lambda v: Vector(v[0], -v[1])
            vect_to_tuple = lambda v: (v[0], v[1])
            entities = simulations[tablist.get_current()].get_entities()
            pygame.draw.line(screen, (0, 0, 255), vect_to_tuple(flip(entities[key].body.get_center())), mouse.get_position(), 2)

    # draw GUI
    draw_tablist(screen)
    draw_toolbar(screen)

    # drawing current tab
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
pygame.font.quit()
