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
        
        self._update_surface_flag = True

        self._gui = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(-3, -3, self._width+6, 67), 
                                                manager=self._manager)
        self._panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(-3, 27, self._width-60, 34), 
                                                  manager=self._manager, 
                                                  container=self._gui)
        
        self._fichier_bt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(-3, -3, 70, 30),
                                                        manager=self._manager,
                                                        text='Fichier',
                                                        container=self._gui,
                                                        object_id=pygame_gui.core.ObjectID(object_id="#fichier_bt"))
        self._param_bt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(62, -3, 90, 30),
                                                      manager=self._manager,
                                                      text='Paramètres',
                                                      container=self._gui,
                                                      object_id=pygame_gui.core.ObjectID(object_id="#param_bt"))
        self._tab_toggle = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(160, -1, 28, 28),
                                                        manager=self._manager,
                                                        text='',
                                                        container=self._gui,
                                                        object_id=pygame_gui.core.ObjectID(class_id="@up_arrow", object_id="#tablist_toggle"))
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
        
    def get_manager(self):
        return self._manager

    def get_current(self):
        return self._current
    
    def set_width(self, width):
        self._width = width
        self._update_surface_flag = True
    
    def get_uflag(self):
        return self._update_surface_flag
    
    def add(self, title, type="test"):
        if title is None:
            title = f"New tab {self._tab_nb}"
        self._tabs.append(Tab(title=title, type=type, id=self._tab_nb, panel=self._panel, tablist=self))
        self._tab_nb += 1
        if self._current == -1:
            self._current = 0
            self._tabs[self._current].state = True
        self._update_surface_flag = True

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
                self._update_surface_flag = True
            elif event.ui_object_id == "panel.#param_bt":
                print('param')
                self._update_surface_flag = True
            elif event.ui_object_id == "panel.#tablist_toggle":
                print('toggle')
                self._update_surface_flag = True
            elif event.ui_object_id == "panel.#tablist_right":
                self._held_right = True
            elif event.ui_object_id == "panel.#tablist_left":
                self._held_left = True
            else:
                for i in range(self._tab_nb):
                    if event.ui_object_id == f"panel.#tab{i}":
                        print(f'tab{i}')
                        self._update_surface_flag = True
                    elif event.ui_object_id == f"panel.#close{i}":
                        print(f'close{i}')
                        self._update_surface_flag = True
        
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id == "panel.#tablist_right":
                self._held_right = False
            elif event.ui_object_id == "panel.#tablist_left":
                self._held_left = False
        
        if self._held_right:
            print('right')
            self._update_surface_flag = True
        if self._held_left:
            print('left')
            self._update_surface_flag = True

        
    def update_surface(self):
        self._update_surface_flag = False
        self._gui.set_dimensions((self._width+6, 67))
        self._panel.set_dimensions((self._width-60, 34))
        self._tab_right.set_relative_position((self._width-33, 30))
        self._tab_left.set_relative_position((self._width-59, 30))
        for i in range(self._tab_nb):
            self._tabs[i].tab_button.set_relative_position((98*i-3 + self._scroll, -3))
            self._tabs[i].close_button.set_relative_position((98*i+61 + self._scroll, -3))

    """def update_scroll(self):
        if self._scroll <= -(len(self._tabs)-1)*self._tab_width:
            self._scroll = min(1-(len(self._tabs)-1)*self._tab_width, 0)"""
    
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
        self.tab_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(-3, -3, 70, 34),
                                                        manager=self.manager,
                                                        text=title,
                                                        container=self.panel,
                                                        object_id=pygame_gui.core.ObjectID(object_id=f"#tab{self.id}"))
        self.close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(62, -3, 34, 34),
                                                          manager=self.manager,
                                                          text='',
                                                          container=self.panel,
                                                          object_id=pygame_gui.core.ObjectID(class_id="@close_bt", object_id=f"#close{self.id}"))
        
    def close(self):
        # Peut-être ouvrir fenêtre pour demander de sauvegarder ?
        pass
