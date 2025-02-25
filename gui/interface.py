import pygame.surface
import pygame_gui.elements.ui_window

import textures

from simulator.controls import Mouse
from gui.button import Button
from gui.text import Text
from gui.tab import Tablist, Tab

import pygame_gui

class Interface:
    def __init__(self, position, size, elements, background = None, color = None, background_relative_position_to_center = (0, 0), relative_positions = []):
        self._position = position
        self._elements = elements
        self._relative_positions = relative_positions
        self._color = color

        self._background_relative_position_to_center = background_relative_position_to_center
        self._background = background

        self._size = None
        self.set_size(size)

    def get_position(self):
        return self._position

    def set_position(self, position):
        if position != self._position:
            self._position = position

            self._update_elements_positions()
            self._update_surface()
    
    def get_size(self):
        return self._size

    def set_size(self, size):
        if size != self._size:
            self._size = size

            self._update_elements_positions()
            self._update_surface()

    def update(self, mouse: Mouse):
        for element in self._elements:
            if type(element) == Button:
                if element.update(mouse):
                    self._update_surface()

    def surface(self):
        return self._surface
    
    def _update_elements_positions(self):
        for i in range(len(self._elements)):
                if type(self._elements[i]) == Button:
                    self._elements[i].set_position((self._position[0]+(self._size[0]-self._elements[i].get_size()[0])//2+self._relative_positions[i][0],
                                                    self._position[1]+(self._size[1]-self._elements[i].get_size()[1])//2+self._relative_positions[i][1]))

    def _update_surface(self):
        self._surface = pygame.Surface((self._size[0], self._size[1]))

        if self._color is not None:
            self._surface.fill(self._color)
        
        if self._background is not None:
            self._surface.blit(self._background, ((self._size[0]-self._background.get_size()[0])//2+self._background_relative_position_to_center[0],
                                                  (self._size[1]-self._background.get_size()[1])//2+self._background_relative_position_to_center[1]))

        for i in range(len(self._elements)):
            if type(self._elements[i]) == Button or type(self._elements[i]) == Text:
                if type(self._elements[i]) == Button:
                    position = ((self._size[0]-self._elements[i].get_size()[0])//2+self._relative_positions[i][0],
                                (self._size[1]-self._elements[i].get_size()[1])//2+self._relative_positions[i][1])
                else:
                    position = ((self._size[0]-self._elements[i].size()[0])//2+self._relative_positions[i][0],
                                (self._size[1]-self._elements[i].size()[1])//2+self._relative_positions[i][1])
                    
                self._surface.blit(self._elements[i].surface(), position)
    
    def __getitem__(self, index):
        return self._elements[index]

# Interface of main menu
main_menu = Interface((0, 30), (pygame.display.get_window_position()[0], pygame.display.get_window_position()[1]-30), [
    Text("Bienvenue sur Newtonian Sandbox !", font_size = 40, color = (0, 0, 0)),
    Button((0, 0), (300, 70), (254, 254, 254), (51, 51, 51), 2, Text("Nouvelle simulation", (51, 51, 51)), (30, 22), hover_text = Text("Nouvelle simulation", (39, 99, 236)), texture = textures.add_button, hover_texture = textures.add_hover_button, texture_position = (250, 24), background_color_on_click = (231, 231, 231)),
    Button((0, 0), (300, 70), (254, 254, 254), (51, 51, 51), 2, Text("Ouvrir une simulation", (51, 51, 51)), (30, 22), hover_text = Text("Ouvrir une simulation", (39, 99, 236)), texture = textures.search, hover_texture = textures.search_hover, texture_position = (250, 24), background_color_on_click = (231, 231, 231)),
], textures.main_background, (254, 254, 254), (-200, 0), [(0, -250), (200, -100), (200, 0)])

# Toolbar
toolbar_manager = pygame_gui.UIManager((2000, 2000), "datas/themes/default.json")
toolbar = [
    pygame_gui.elements.UIButton(relative_rect = pygame.Rect((-2, -2), (100, 36)), text = 'Fichiers', manager = toolbar_manager),
    pygame_gui.elements.UIButton(relative_rect = pygame.Rect((90, -2), (100, 36)), text = 'Paramètres', manager = toolbar_manager),
]

# Tablist
tablist = Tablist(Tab.minimal_size, (0, 30))
toggle_tablist_button = Button((-25, 0), (25, 32), Tab.background_color, Tab.border_color, 2, texture = textures.arrow_down, hover_texture = textures.arrow_hover_down, background_color_on_click = (231, 231, 231))
toggle_tablist = False

creating_simulation = False

def update_tablist_events(mouse: Mouse):
    global toggle_tablist, toggle_tablist_button, main_menu

    toggle_tablist_button.update(mouse)

    if toggle_tablist:
        tablist.update(mouse)

def update_toolbar_events(event):
    global toggle_tablist, main_menu, creating_simulation

    toolbar_manager.process_events(event)

    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == toolbar[1]:
            toggle_tablist = True
            tablist.add("Paramètres")
    elif event.type == pygame.WINDOWRESIZED:
        width, height = pygame.display.get_window_size()
        update_toolbar_position(width)
        update_tablist_position(width, height)
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if toggle_tablist_button.is_hover() and pygame.mouse.get_just_pressed()[0]:
            toggle_tablist = not(toggle_tablist)
            main_menu.set_size((tablist.get_width(), main_menu.get_size()[1]+(-1)**(toggle_tablist)*24))
            main_menu.set_position((0, 30+24*toggle_tablist))
    
        if main_menu[1].is_hover() and pygame.mouse.get_just_pressed()[0] and not(creating_simulation):
            popup_width, popup_height = 400, 300
            screen_size = pygame.display.get_window_size()
            popup = pygame_gui.elements.ui_window.UIWindow(pygame.Rect((screen_size[0]-popup_width)//2, (screen_size[1]-popup_height)//2, popup_width, popup_height), manager = toolbar_manager, window_display_title = "Nouvelle simulation", draggable = False)
            
            # Saisie pour le nom
            pygame_gui.elements.UITextBox("Nom :", pygame.Rect(20, 0, 70, 30), container = popup, visible = 0)
            name_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(90, 0, 70, 30), initial_text = "nouvelle simulation", container = popup)

            # Faire les autres saisies (globalement un copié-collé puis chercher sur internet)
            
            creating_simulation = True
            toggle_tablist = True
            

def update_tablist_position(width, height):
    global tablist, toggle_tablist, toggle_tablist_button, main_menu

    toggle_tablist_button.set_position((width-25, 0))
    tablist.set_width(width)
    main_menu.set_size((width, height-30-24*toggle_tablist))

def update_toolbar_position(width):
    global toolbar_manager
    toolbar_manager.set_window_resolution((width, 30))

def draw_tablist(surface):
    global toggle_tablist, toggle_tablist_button

    if toggle_tablist:
        toggle_tablist_button.set_texture(textures.arrow_up)
        toggle_tablist_button.set_hover_texture(textures.arrow_hover_up)

        surface.blit(tablist.surface(), tablist.get_position())
        pygame.draw.line(surface, Tab.border_color, (0, 52), (surface.get_size()[0], 52), 2)
        pygame.draw.line(surface, Tab.border_color, (0, 30), (surface.get_size()[0], 30), 2)
    else:
        toggle_tablist_button.set_texture(textures.arrow_down)
        toggle_tablist_button.set_hover_texture(textures.arrow_hover_down)

def draw_toolbar(surface):
    global toggle_tablist, toggle_tablist_button, toolbar_manager

    pygame.draw.rect(surface, Tab.background_color, (0, 0, surface.get_size()[0], 30))
    pygame.draw.line(surface, Tab.border_color, (0, 0), (surface.get_size()[0], 0), 2)

    toolbar_manager.draw_ui(surface)

    surface.blit(toggle_tablist_button.surface(), toggle_tablist_button.get_position())

    if not(toggle_tablist):
        pygame.draw.line(surface, Tab.border_color, (0, 30), (surface.get_size()[0], 30), 2)

update_tablist_position(*pygame.display.get_window_size())

# tabs content
tabs_content = []
