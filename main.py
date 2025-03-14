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
simulations[0].add_entity(Entity(Vector(100, 0), Circle(Vector(100, -200), 50), 0.100001))
simulations[0].add_entity(Entity(Vector(-100, 0), Circle(Vector(600, -200), 50), 0.1))

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

    # updating current tab
    if tablist.get_current() == -1:
        main_menu.update(mouse)
        screen.blit(main_menu.surface(), main_menu.get_position())
    else:
        simulations[tablist.get_current()].update()
        simulations[tablist.get_current()].display_on(screen)

    # draw GUI
    draw_tablist(screen)
    draw_toolbar(screen)

    # drawing current tab
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
pygame.font.quit()
