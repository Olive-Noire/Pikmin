import pygame.surface

import gui
from simulator.controls import Mouse

class Button:
    def __init__(self, position: tuple, size: tuple, background_color = (0, 0, 0, 255), border_color = None, border_size = 0, text = None, text_posisition = None, texture = None, texture_position = None, hover_text = None, hover_texture = None, background_color_on_click = None):
        self._position = position
        self._size = size

        self._background_color = background_color
        self._background_color_on_click = background_color_on_click

        self._border_color = border_color
        self._border_size = border_size

        self._text = text
        self._hover_text = hover_text
        self._text_posisition = text_posisition

        self._texture = texture
        self._hover_texture = hover_texture
        self._texture_position = texture_position

        self._click = self._hover = False

        self._surface = pygame.Surface(self._size)

        if gui.track_updates:
            gui.log("updating button texture (change of size)")
        self._update_surface()

        self._text_properties = None
    
    def get_position(self):
        return self._position
    
    def set_position(self, position):
        self._position = position
    
    def get_size(self):
        return self._size
    
    def set_size(self, size):
        if self._size != size:
            self._size = size

            if gui.track_updates:
                gui.log("updating button texture (change of size)")
            self._update_surface()
    
    def get_background_color(self):
        return self._background_color
    
    def set_background_color(self, background_color):
        if self._background_color != background_color:
            self._background_color = background_color

            if gui.track_updates:
                gui.log("updating button texture (change of background color)")
            self._update_surface()

            return True
        
        return False
    
    def get_border_color(self):
        return self._border_color
    
    def set_border_color(self, border_color):
        if self._border_color != border_color:
            self._border_color = border_color

            if gui.track_updates:
                gui.log("updating button texture (change of border color)")
            self._update_surface()
    
    def get_border_size(self):
        return self._border_size
    
    def set_border_size(self, border_size):
        if self._border_size != border_size:
            self._border_size = border_size

            if gui.track_updates:
                gui.log("updating button texture (change of border size)")
            self._update_surface()
    
    @property
    def text(self):
        self._text_properties = (self._text.get_content(), self._text.get_color(), self._text.get_font(), self._text.get_font_size())
        return self._text
    
    def get_text_posisition(self):
        return self._text_posisition
    
    def set_text_position(self, text_position):
        if self._text_posisition != text_position:
            self._text_posisition = text_position

            if gui.track_updates:
                gui.log("updating button texture (change of text position)")
            self._update_surface()
    
    def get_texture_posisition(self):
        return self._texture_posisition
    
    def set_texture_posisition(self, texture_posisition):
        if self._texture_posisition != texture_posisition:
            self._texture_posisition = texture_posisition

            if gui.track_updates:
                gui.log("updating button texture (change of texture position)")
            self._update_surface()

    def get_texture(self):
        return self._texture

    def set_texture(self, texture: pygame.Surface):
        if self._texture != texture:
            self._texture = texture

            if gui.track_updates:
                gui.log("updating button texture (change of texture)")
            self._update_surface()

            return True
        
        return False
    
    def get_hover_texture(self):
        return self._texture
    
    def set_hover_texture(self, hover_texture):
        if self._hover_texture != hover_texture:
            self._hover_texture = hover_texture

            if gui.track_updates:
                gui.log("updating button texture (change of hover texture)")
            self._update_surface()

    def is_hover(self):
        return self._hover

    def is_click(self):
        return self._click
    
    def update(self, mouse: Mouse):
        hover = self._position[0] <= mouse.get_position()[0] <= self._position[0]+self._size[0] and self._position[1] <= mouse.get_position()[1] <= self._position[1]+self._size[1]
        click = self._hover and mouse.left_click()

        if hover != self._hover or click != self._click:
            self._hover = hover
            self._click = click

            self._update_surface()
            return True
        
        return False
    
    def surface(self):
        if self._text_properties is not None and self._text_properties != (self._text.get_content(), self._text.get_color(), self._text.get_font(), self._text.get_font_size()):
            if gui.track_updates:
                gui.log("updating button texture (change of text)")
            self._update_surface()

            self._text_properties = None

        return self._surface
    
    def _update_surface(self):
        if self._size != self._surface.get_size():
            self._surface = pygame.Surface(self._size)

        if self._click and self._background_color_on_click is not None:
            self._surface.fill(self._background_color_on_click)
        else:
            self._surface.fill(self._background_color)

        if self._text is not None and (self._hover_text is None or not(self._hover)):
            text_position = self._text_posisition
            if text_position is None:
                text_size = self._text.size()
                text_position = ((self._size[0]-text_size[0])//2, (self._size[1]-text_size[1])//2)

            self._surface.blit(self._text.surface(), text_position)
        
        if self._hover_text is not None and self._hover:
            text_position = self._text_posisition
            if text_position is None:
                text_size = self._hover_text.size()
                text_position = ((self._size[0]-text_size[0])//2, (self._size[1]-text_size[1])//2)

            self._surface.blit(self._hover_text.surface(), text_position)

        if self._texture is not None and (self._hover_texture is not None or not(self._hover)):
            texture_position = self._texture_position
            if texture_position is None:
                texture_size = self._texture.get_rect().size
                texture_position = ((self._size[0]-texture_size[0])//2, (self._size[1]-texture_size[1])//2)
            self._surface.blit(self._texture, texture_position)
        
        if self._hover_texture is not None and self._hover:
            texture_position = self._texture_position
            if texture_position is None:
                texture_size = self._texture.get_rect().size
                texture_position = ((self._size[0]-texture_size[0])//2, (self._size[1]-texture_size[1])//2)
                
            self._surface.blit(self._hover_texture, texture_position)
        
        if self._border_color is not None:
            pygame.draw.rect(self._surface, self._border_color, rect = (0, 0, *self._size), width = self._border_size)