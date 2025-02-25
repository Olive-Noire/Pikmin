import pygame.surface

import textures

import gui
from gui.text import Text
from gui.button import Button

from simulator.controls import Mouse

class Tab:
    text_color = (75, 75, 75)
    text_hover_color = (39, 99, 236)

    background_color = (254, 254, 254)
    background_click_color = (231, 231, 231)

    border_color = (75, 75, 75)

    minimal_size = 70

    def __init__(self, title):
        self._title = Text(title, Tab.text_color, font_size = 15)
        self._width = 0

        self._hover_close = self._hover = False
        self._click = self._click_down = False

        self._state = False

        if gui.track_updates:
            gui.log("updating tab texture (initialization)")
        self._update_surface()

    def get_state(self):
        return self._state

    def set_state(self, state):
        if state != self._state:
            self._state = self._click = state
            self._update_surface()

    def get_title(self):
        return self._title.get_content()
    
    def set_title(self, title):
        if self._title.get_content() != title:
            self._title.set_content(title)

            if gui.track_updates:
                gui.log("updating tab texture (change of title)")
            self._update_surface()

    def is_click_close(self):
        return self._hover_close and self._click

    def is_click_down_close(self):
        return self._hover_close and self._click_down

    def is_click(self):
        return self._click

    def is_click_down(self):
        return self._click_down
    
    def is_hover_close(self):
        return self._hover_close
    
    def is_hover(self):
        return self._hover
    
    def update(self, virtual_position: tuple, mouse: Mouse):
        hover = virtual_position[0] <= mouse.get_position()[0] <= virtual_position[0]+self._width \
                and virtual_position[1] <= mouse.get_position()[1] <= virtual_position[1]+24

        close_hover = virtual_position[0]+self._width-20 <= mouse.get_position()[0] <= virtual_position[0]+self._width-8 \
                    and virtual_position[1]+6 <= mouse.get_position()[1] <= virtual_position[1]+18

        update_surface_flag = False
        if close_hover:
            if not(self._hover_close):
                self._hover_close = True
                update_surface_flag = True
        elif self._hover_close:
            self._hover_close = False
            update_surface_flag = True

        if hover:
            if not(self._hover):
                self._hover = True
                update_surface_flag = True
            
            if mouse.left_click_down():
                if not(self._click_down):
                    self._click_down = self._state = True
                    update_surface_flag = True
            elif self._click_down:
                self._click_down = False
            
            if not(self._click) and mouse.left_click():
                self._click = True
                update_surface_flag = True
            elif self._click and not(mouse.left_click()):
                self._click = False
                update_surface_flag = True
        elif self._hover:
            self._hover = False
            update_surface_flag = True
                
        if update_surface_flag:
            if gui.track_updates:
                gui.log("updating tab texture (hover or click)")
            self._update_surface()
        
        return update_surface_flag
        
    def surface(self, width):
        assert(width >= Tab.minimal_size)

        if self._width != width:
            self._width = width

            if gui.track_updates:
                gui.log("updating tab texture (change of width)")
            self._update_surface()
    
        return self._surface
    
    def _update_surface(self):
        self._surface = pygame.Surface((self._width, 24))

        if (self._click and self._hover) or self._state:
            self._surface.fill(Tab.background_click_color)
        else:
            self._surface.fill(Tab.background_color)

        if self._hover or self._state:
            self._title.set_color(Tab.text_hover_color)
        else:
            self._title.set_color(Tab.text_color)

        self._surface.blit(self._title.surface(), (10, 2, *self._title.size()))

        if (self._click and self._hover) or self._state:
            pygame.draw.rect(self._surface, Tab.background_click_color, (self._width-22, 0, 22, 20))
        else:
            pygame.draw.rect(self._surface, Tab.background_color, (self._width-22, 0, 22, 20))

        if self._hover_close:
            self._surface.blit(textures.close_hover_button, (self._width-20, 6, 12, 12))
        else:
            self._surface.blit(textures.close_button, (self._width-20, 6, 12, 12))
        
        pygame.draw.rect(self._surface, Tab.border_color, (0, 0, self._width, 24), 1)

class Tablist:
    background_color = (231, 231, 231)
    scroll_sensibility = 7
    
    def __init__(self, width: int, position: tuple, tabs = []):
        assert(width >= Tab.minimal_size)

        self._tabs = tabs
        self._width = width
        self._position = position

        self._current = -1
        if len(self._tabs) > 0:
            self._current = 0
            self._tabs[0].set_state(True)

        self._scroll = 0
        self._tab_width = min(max(13*self._width/88+120/11, Tab.minimal_size), 200)

        self._arrows = [
            Button(None, (24, 24), Tab.background_color, Tab.border_color, 1, texture = textures.arrow_right, hover_texture = textures.arrow_hover_right, background_color_on_click = (231, 231, 231)),
            Button(None, (24, 24), Tab.background_color, Tab.border_color, 1, texture = textures.arrow_left, hover_texture = textures.arrow_hover_left, background_color_on_click = (231, 231, 231)),
        ]

        if gui.track_updates:
            gui.log("updating tab list texture (initialization)")
        self._surface = pygame.Surface((0, 0))
        self._update_surface()
    
    def get_current(self):
        return self._current

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position
    
    def get_width(self):
        return self._width
    
    def set_width(self, width):
        assert(width >= Tab.minimal_size)

        if self._width != width:
            self._width = width
            self._tab_width = min(max(13*self._width/88+120/11, Tab.minimal_size), 200)
            self._update_scroll()

            if gui.track_updates:
                gui.log("updating tab list texture (change of width)")
            self._update_surface()
    
    def add(self, title):
        self._tabs.append(Tab(title))

        if self._current == -1:
            self._current = 0
            self._tabs[self._current].set_state(True)

        if gui.track_updates:
            gui.log("updating tab list texture (adding new tab)")
        self._update_surface()
    
    def update(self, mouse: Mouse):
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
        
        if update_surface_flag:
            if gui.track_updates:
                gui.log("updating tab list texture (interaction)")
            self._update_surface()
        
        return to_delete

    def surface(self):
        return self._surface

    def _update_scroll(self):
        if self._scroll <= -(len(self._tabs)-1)*self._tab_width:
                self._scroll = min(1-(len(self._tabs)-1)*self._tab_width, 0)

    def _update_surface(self):
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
        self._surface.blit(self._arrows[1].surface(), (self._width-48, 0))
    
    def __getitem__(self, index):
        return self._tabs[index]