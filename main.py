# Pygame
import pygame
pygame.init()
pygame.font.init()

width, height = 1920, 1017
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Newtonian Sandbox")

# GUI
from gui.interface import *
import gui.interface
from gui import tick

# Simulator
from simulator.controls import *
mouse = Mouse()
keyboard = Keyboard()

clock = pygame.time.Clock()

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

    # draw GUI
    draw_tablist(screen)
    draw_toolbar(screen)

    # drawing current tab
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
pygame.font.quit()