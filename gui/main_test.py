import pygame
import pygame_gui.ui_manager
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

import pygame_gui
manager = pygame_gui.ui_manager.UIManager(window_resolution=(width, height), theme_path="datas/themes/default.json",)
panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(0, 10, 300, 34), manager=manager)
pygame_gui.elements.UIButton(relative_rect=pygame.Rect(300-33, 0, 28, 28),
                            manager=manager,
                            text='',
                            container=panel,
                            object_id=pygame_gui.core.ObjectID(class_id="@right_arrow", object_id="#tablist_right")),
pygame_gui.elements.UIButton(relative_rect=pygame.Rect(300-59, 0, 28, 28),
                            manager=manager,
                            text='',
                            container=panel,
                            object_id=pygame_gui.core.ObjectID(class_id="@left_arrow", object_id="#tablist_left")),
pygame_gui.elements.UIButton(relative_rect=pygame.Rect(-3, -3, 70, 33),
                             manager=manager,
                             text='Tab test',
                             container=panel)
pygame_gui.elements.UIButton(relative_rect=pygame.Rect(68, 0, ),
                             manager=manager,
                             text='',
                             container=panel,
                             object_id=pygame_gui.core.ObjectID(class_id="@close_bt", object_id="#tablist_close"))


run = True
while run:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        manager.process_events(event)
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id == "panel.#tablist_left":
                print('mdr')
        
        mouse.update(event)
        keyboard.update(event)
        
    if keyboard.key_down('f11'):
        pygame.display.toggle_fullscreen()
    
    manager.update(time_delta)
    screen.blit(background, (0,0))
    manager.draw_ui(screen)
    
    pygame.display.update()