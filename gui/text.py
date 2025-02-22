import pygame.font

class Text:
    default_font = pygame.font.get_fonts()[0]

    if "associatesansmedium" in pygame.font.get_fonts():
        default_font = "associatesansmedium"

    def __init__(self, content, color = (255, 255, 255), font_name = default_font, font_size = 20):
        self._color = color
        self._font_name = font_name
        self._font_size = font_size
        self._content = content

        self._update_font()
        self._update_surface()
    
    def get_font(self):
        return self._font_name
    
    def set_font(self, font_name):
        self._font_name = font_name
        self._update_font()
    
    def get_font_size(self):
        return self._font_size

    def set_font_size(self, font_size):
        self._font_size = font_size
        self._update_font()

    def get_content(self):
        return self._content
    
    def set_content(self, content: str):
        self._content = content
        self._update_surface()
    
    def get_color(self):
        return self._color
    
    def set_color(self, color: tuple):
        self._color = color
        self._update_surface()

    def surface(self):
        return self._surface

    def size(self):
        return self._font.size(self._content)
    
    def _update_font(self):
        self._font = pygame.font.SysFont(self._font_name, self._font_size)

    def _update_surface(self):
        self._surface = self._font.render(self._content, True, self._color)