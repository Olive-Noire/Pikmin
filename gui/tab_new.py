import pygame
import pygame_gui
import pygame_gui.ui_manager

class Tablist:
    def __init__(self, width: int, position: tuple, manager: pygame_gui.ui_manager, tabs: list = []):
        self._tabs = tabs
        self._width = width
        self._position = position
        self._manager = manager

        self._current = -1
        if len(self._tabs) > 0:
            self._current = 0
            self._tabs[0].set_state(True)

        self._scroll = 0
        self._tab_width = min(max(13*self._width/88+120/11, Tab.minimal_size), 200)
        
        self._update_surface_flag = False

        self._panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(0, 10, self._width, 34), manager=manager)
        self._arrows = [
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect(self._width-33, 0, 28, 28),
                                         manager=self._manager,
                                         text='',
                                         object_id=pygame_gui.core.ObjectID(class_id="@right_arrow", object_id="#tablist_right")),
            pygame_gui.elements.UIButton(relative_rect=pygame.Rect(self._width-59, 0, 28, 28),
                                         manager=self._manager,
                                         text='',
                                         object_id=pygame_gui.core.ObjectID(class_id="@left_arrow", object_id="#tablist_left")),
        ]
    
    def get_current(self):
        return self._current

    def get_position(self):
        return self._position

    def set_position(self, position: tuple):
        self._position = position
    
    def get_width(self):
        return self._width
    
    def set_width(self, width: int):
        assert(width >= Tab.minimal_size)

        if self._width != width:
            self._width = width
            self._tab_width = min(max(13*self._width/88+120/11, Tab.minimal_size), 200)
            self._update_surface_flag = True
    
    def update_flag(self):
        return self._update_surface_flag
    
    def add(self, title, type):
        self._tabs.append(Tab(title, type, self))

        if self._current == -1:
            self._current = 0
            self._tabs[self._current].set_state(True)
        self._update_surface_flag = True

    """def update(self, mouse: Mouse):
        update_surface_flag = False
        to_delete = None

        for i in [0, 1]:
            self._arrows[i].set_position((self._position[0]+self._width-24*(1+i)-1+i, self._position[1]))
            if self._arrows[i].update(mouse):
                update_surface_flag = True

            if self._arrows[i].is_click():
                if (i == 0 and self._scroll > -(len(self._tabs)-1)*self._tab_width) or (i == 1 and self._scroll < 0):
                    self._scroll -= Tablist.scroll_sensibility*(-1)**i
                    update_surface_flag = True
        
        for i in range(len(self._tabs)):
            if self._tab_width*(i+1)+self._scroll < 0:
                continue

            if self._tab_width*i+self._scroll > self._width:
                break

            if self._width-48 > mouse.get_position()[0] and self._position[1] <= mouse.get_position()[1] <= self._position[1]+24:
                if self._tabs[i].update((self._position[0]+self._tab_width*i+self._scroll, self._position[1]), mouse):
                    update_surface_flag = True

                    if self._tabs[i].get_state() and self._current != i and not(self._tabs[i].is_hover_close()):
                        self._tabs[self._current].set_state(False)
                        self._current = i
                    
                    if self._tabs[i].is_click_down_close():
                        to_delete = i
            else:
                if self._tabs[i].is_hover():
                    self._tabs[i].update((0, -25), mouse)
                    update_surface_flag = True

        
        if to_delete is not None:
            del self._tabs[to_delete]
            if self._current >= to_delete:
                self._current -= 1

                if to_delete == 0:
                    if len(self._tabs) > 0:
                        self._current = 0

                if self._current >= 0:
                    self._tabs[self._current].set_state(True)
            
            self._update_scroll()

            update_surface_flag = True         
        
        return to_delete"""
    
    def surface(self):
        return self._surface

    def update_scroll(self):
        if self._scroll <= -(len(self._tabs)-1)*self._tab_width:
                self._scroll = min(1-(len(self._tabs)-1)*self._tab_width, 0)

    """def _update_surface(self):
        if self._width != self._surface.get_size()[0]:
            self._surface = pygame.Surface((self._width, 24))
        
        self._surface.fill(Tablist.background_color)

        for i in range(len(self._tabs)):
            if self._tab_width*(i+1)+self._scroll < 0:
                continue

            self._surface.blit(self._tabs[i].surface(self._tab_width), (self._tab_width*i+self._scroll, 0))

            if self._tab_width*(i+1)+self._scroll > self._width:
                break
        
        self._surface.blit(self._arrows[0].surface(), (self._width-24, 0))
        self._surface.blit(self._arrows[1].surface(), (self._width-48, 0))"""
    
    def __getitem__(self, index):
        return self._tabs[index]

class Tab:
    minimal_size = 70
    def __init__(self, title: str, type: str, tablist: Tablist):
        self._title = pygame_gui.elements.UILabel()
        self._width = 0
        
        self._type = type
        