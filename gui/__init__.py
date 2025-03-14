from termcolor import colored

import pygame.time

def log(message):
    print(colored("GUI :", "cyan"), message+".")

# settings
gui_clock = pygame.Clock()
tick = gui_clock.tick(60)/1000.0

# fonts
log("loading fonts...")
# import gui.fonts

# flags
track_updates = False
