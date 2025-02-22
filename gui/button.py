import pygame.surface

from simulator.controls import Mouse

class Button:
    def __init__(self, position: tuple, size: tuple, background_color = (0, 0, 0, 255), border_color = None, border_size = 1, text = None, text_posisition = None, texture = None, texture_position = None):
        self._position = position
        self._size = size

        self._background_color = background_color

        self._border_color = border_color
        self._border_size = border_size

        self._text = text
        self._text_posisition = text_posisition

        self._texture = texture
        self._texture_position = texture_position

        self._surface = pygame.Surface(self._size)
        self._update_surface()

        self._edited_content = False
    
    def get_position(self):
        return self._position
    
    def set_position(self, position):
        self._position = position
    
    def get_size(self):
        return self._size
    
    def set_size(self, size):
        self._size = size
    
    def get_background_color(self):
        return self._background_color
    
    def set_background_color(self, background_color):
        self._background_color = background_color
    
    def get_border_color(self):
        return self._border_color
    
    def set_border_color(self, border_color):
        self._border_color = border_color
    
    def get_border_size(self):
        return self._border_size
    
    def set_border_size(self, border_size):
        self._border_size = border_size
    
    @property
    def text(self):
        self._edited_content = True
        return self._text
    
    def get_text_posisition(self):
        return self._text_posisition
    
    def set_text_position(self, text_position):
        self._text_posisition = text_position
    
    def get_texture_posisition(self):
        return self._texture_posisition
    
    def set_texture_posisition(self, texture_posisition):
        self._texture_posisition = texture_posisition

    def get_texture(self):
        return self._texture

    def set_texture(self, texture: pygame.Surface):
        self._texture = texture

    def is_hover(self, mouse: Mouse):
        return self._position[0] <= mouse.get_position()[0] <= self._position[0]+self._size[0] and self._position[1] <= mouse.get_position()[1] <= self._position[1]+self._size[1]

    def is_click(self, mouse: Mouse):
        return self.is_hover(mouse) and mouse.left_click_down()
    
    def surface(self):
        if self._edited_content:
            self._update_surface()
            self._edited_content = False

        return self._surface
    
    def _update_surface(self):
        self._surface.fill(self._background_color)

        if self._text is not None:
            text_posisition = self._text_posisition
            if text_posisition is None:
                text_size = self._text.size()
                text_posisition = ((self._size[0]-text_size[0])//2, (self._size[1]-text_size[1])//2)

            self._surface.blit(self._text.surface(), text_posisition)

        if self._texture is not None:
            texture_position = self._texture_position
            if texture_position is None:
                texture_size = self._texture.get_rect().size
                texture_position = ((self._size[0]-texture_size[0])//2, (self._size[1]-texture_size[1])//2)

            self._surface.blit(self._texture, texture_position)
        
        if self._border_color is not None:
            pygame.draw.rect(self._surface, self._border_color, rect = (*self._position, 100, 100), width = self._border_size)