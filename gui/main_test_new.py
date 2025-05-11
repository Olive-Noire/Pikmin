import sys

import pygame_gui.elements.ui_label
sys.path.append("D:/Travail/Tle/NSI/Pikmin-main")

import pygame
import pygame_gui
pygame.init()

width, height = 1000, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Pysics")
background = pygame.Surface((width, height))
background.fill("cyan")

from simulator.controls import Mouse, Keyboard
mouse = Mouse()
keyboard = Keyboard()

clock = pygame.time.Clock()

import pygame_gui.ui_manager
from tab_new import Tab, Tablist
tab_manager = pygame_gui.ui_manager.UIManager(window_resolution=(width, height),
                                              theme_path="datas/themes/default.json")
tablist = Tablist(width, tab_manager)

run = True
while run:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        tablist.update(event)
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.WINDOWRESIZED:
            tablist.set_width(screen.get_width())
        
        mouse.update(event)
        keyboard.update(event)
        
    if keyboard.key_down('f11'):
        pygame.display.toggle_fullscreen()
    
    if keyboard.key_down('k'):
        tablist.add(None)
        
    tab_manager.update(time_delta)
    screen.blit(background, (0,0))
    if tablist.get_uflag():
        tablist.update_surface()
    tab_manager.draw_ui(screen)
    pygame.display.update()
