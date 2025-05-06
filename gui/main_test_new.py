import sys
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

from tab_new import Tab, Tablist
tab_manager = pygame_gui.ui_manager.UIManager
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
    
    screen.blit(background, (0,0))
    if tablist.get_uflag():
        tablist.update_surface()
    
    pygame.display.update()
