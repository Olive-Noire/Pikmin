import pygame
import pygame_gui
import pygame_gui.ui_manager

class Tablist:
    def __init__(self, width: int, manager: pygame_gui.ui_manager.UIManager):
        self._tabs = []
        self._current = -1
        self._tab_nb = 0
        
        self._manager = manager

        self._scroll = 0
        self._width = width
        
        self._usf = True
        self._usc = True

        self._gui = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(-3, -3, self._width+6, 67), 
                                                manager=self._manager)
        self._panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(-3, 27, self._width-60, 34), 
                                                  manager=self._manager, 
                                                  container=self._gui)
        
        self._fichier_bt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(-3, 0, 70, 30),
                                                        manager=self._manager,
                                                        text='Fichier',
                                                        container=self._gui,
                                                        object_id=pygame_gui.core.ObjectID(object_id="#fichier_bt"))
        self._param_bt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(62, 0, 90, 30),
                                                      manager=self._manager,
                                                      text='Paramètres',
                                                      container=self._gui,
                                                      object_id=pygame_gui.core.ObjectID(object_id="#param_bt"))
        self._tab_toggle = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(160, 1, 28, 28),
                                                        manager=self._manager,
                                                        text='',
                                                        container=self._gui,
                                                        object_id=pygame_gui.core.ObjectID(class_id="@up_arrow", object_id="#panel_container.#tablist_up"))
        self._tab_right = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(width-33, 30, 28, 28),
                                                       manager=self._manager,
                                                       text='',
                                                       container=self._gui,
                                                       object_id=pygame_gui.core.ObjectID(class_id="@right_arrow", object_id="#tablist_right"))
        self._tab_left = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(width-59, 30, 28, 28),
                                                      manager=self._manager,
                                                      text='',
                                                      container=self._gui,
                                                      object_id=pygame_gui.core.ObjectID(class_id="@left_arrow", object_id="#tablist_left"))
        
        self._held_right = False
        self._held_left = False
        self._full = True
        
    def get_manager(self):
        return self._manager

    def get_current(self):
        return self._current
    
    def set_width(self, width):
        self._width = width
        self._usf = True
    
    def get_usf(self):
        return self._usf
    
    def get_usc(self):
        return self._usc
    
    def add(self, title, type="test"):
        if title is None:
            title = f"New tab {self._tab_nb}"
        self._tabs.append(Tab(title=title, type=type, id=self._tab_nb, panel=self._panel, tablist=self))
        self._tab_nb += 1
        if self._current == -1:
            self._current = 0
            self._tabs[self._current].state = True
        self._usc = True

    def close(self, id):
        closed = self._tabs.pop(id)
        closed.close()
        self._tab_nb -= 1
        for i in range(id, self._tab_nb):
            self._tabs[i].set_id(i)
            self._tabs[i].tab_button.change_object_id(pygame_gui.core.ObjectID(object_id=f"#tab{i}"))
            self._tabs[i].close_button.change_object_id(pygame_gui.core.ObjectID(class_id="@close_bt", object_id=f"#close{i}"))
    
    def update(self, event):
        self._manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_object_id == "panel.#fichier_bt":
                print('fichier')
                self._usf = True
            elif event.ui_object_id == "panel.#param_bt":
                print('param')
                self._usf = True

            elif event.ui_object_id == "panel.#panel_container.#tablist_up":
                print('toggle')
                self._full = False
                self._tab_toggle.change_object_id(pygame_gui.core.ObjectID(class_id="@down_arrow", object_id="#tablist_down"))
                self._usf = True
            elif event.ui_object_id == "panel.#panel_container.#tablist_down":
                print('toggle')
                self._full = True
                self._tab_toggle.change_object_id(pygame_gui.core.ObjectID(class_id="@up_arrow", object_id="#tablist_up"))
                self._usf = True
                
            elif event.ui_object_id == "panel.#tablist_right":
                self._held_right = True
            elif event.ui_object_id == "panel.#tablist_left":
                self._held_left = True
                
            elif event.ui_object_id[:16] == "panel.panel.#tab":
                i = int(event.ui_object_id[16:])
                print(f'tab{i}')
                self._usf = True
            
            elif event.ui_object_id[:18] == "panel.panel.#close":
                i = int(event.ui_object_id[18:])
                print(f'close{i}')
                self._usf = True
        
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id == "panel.#tablist_right":
                self._held_right = False
            elif event.ui_object_id == "panel.#tablist_left":
                self._held_left = False
        
        if self._held_right:
            print('right')
            self._scroll += 1
            self._usc = True
        if self._held_left:
            print('left')
            self._scroll -= 1
            self._usc = True

        
    def update_surface(self):
        self._usf = False
        if self._full:
            self._gui.set_dimensions((self._width+6, 67))
        else:
            self._gui.set_dimensions((self._width+6, 34))
        self._panel.set_dimensions((self._width-60, 34))
        self._tab_right.set_relative_position((self._width-33, 30))
        self._tab_left.set_relative_position((self._width-59, 30))
        

    def update_scroll(self):
        self._usc = False
        if self._tab_nb*118 > self._width-60 and self._tab_nb*118 - self._scroll < self._width-60:
            self._scroll -= 1
        if self._scroll < 0:
            self._scroll = 0
        
        for i in range(self._tab_nb):
            self._tabs[i].tab_button.set_relative_position((118*i-3 + self._scroll, -3))
            self._tabs[i].close_button.set_relative_position((118*i+81 + self._scroll, -3))
    
    def __getitem__(self, index):
        return self._tabs[index]
    
class Tab:
    minimal_size = 70
    def __init__(self, title: str, type: str, id: int, panel, tablist: Tablist):
        self.id = id
        self.state = False
        
        self.type = type
        self.title = title
        
        self.manager = tablist.get_manager()
        self.panel = panel
        self.tab_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(-3, -3, 90, 34),
                                                        manager=self.manager,
                                                        text=title,
                                                        container=self.panel,
                                                        object_id=pygame_gui.core.ObjectID(object_id=f"#tab{self.id}"))
        self.close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(82, -3, 34, 34),
                                                          manager=self.manager,
                                                          text='',
                                                          container=self.panel,
                                                          object_id=pygame_gui.core.ObjectID(class_id="@close_bt", object_id=f"#close{self.id}"))
        
    def close(self):
        # Peut-être ouvrir fenêtre pour demander de sauvegarder ?
        pass
