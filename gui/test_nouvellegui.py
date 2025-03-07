import pygame
import pygame_gui


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600), flags=pygame.RESIZABLE)

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

pikmin = pygame_gui.elements.UIWindow(rect=pygame.Rect(50, 50, 400, 270),
                                      manager=manager,
                                      window_display_title="Nouvelle Simulation",
                                      draggable=False)

name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(30, 30, 50, 30), text="Nom :", manager=manager, container=pikmin)
name_input = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect(90, 30, 250, 30), manager=manager, container=pikmin)
dt_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(30, 90, 50, 30), text="dt :", manager=manager, container=pikmin)
dt_input = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect(90, 90, 80, 30), manager=manager, container=pikmin)
fps_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(180, 90, 50, 30), text="/ FPS :", manager=manager, container=pikmin)
fps_input = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect(240, 90, 80, 30), manager=manager, container=pikmin)
fluid_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(30, 150, 50, 30), text="Fluide :", manager=manager, container=pikmin)
fluid_input = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(90, 150, 150, 30), options_list=['None', 'Test'], starting_option='None', manager=manager, container=pikmin)


clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == "test":
                pass

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
pygame.quit()
