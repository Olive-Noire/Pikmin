import pygame.mouse

class Mouse:
    def __init__(self):
        self._position = (0, 0)

        self._right_click = self._wheel_click = self._left_click = False
        self.clear()

        self._wheel = self._wheel_change = 0

    def update(self, event: pygame.event):
        if event.type == pygame.MOUSEMOTION:
            self._position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._update_clicks()

            self._left_click_down = pygame.mouse.get_pressed()[0]
            self._wheel_click_down = pygame.mouse.get_pressed()[1]
            self._right_click_down = pygame.mouse.get_pressed()[2]
        elif event.type == pygame.MOUSEBUTTONUP:
            self._update_clicks()
            
            self._left_click_up = pygame.mouse.get_pressed()[0]
            self._wheel_click_up = pygame.mouse.get_pressed()[1]
            self._right_click_up = pygame.mouse.get_pressed()[2]
        elif event.type == pygame.MOUSEWHEEL:
            self._wheel_change = event.y
            self._wheel += self._wheel_change
    
    def clear(self):
        self._right_click_down = self._wheel_click_down = self._left_click_down = False
        self._right_click_up = self._wheel_click_up = self._left_click_up = False
    
    def left_click(self):
        return self._left_click
    
    def left_click_down(self):
        return self._left_click_down
    
    def left_click_up(self):
        return self._left_click_up
    
    def wheel_click(self):
        return self._wheel_click

    def wheel_click_down(self):
        return self._wheel_click_down

    def wheel_click_up(self):
        return self._wheel_click_up

    def right_click(self):
        return self._right_click

    def right_click_down(self):
        return self._right_click_down
    
    def right_click_up(self):
        return self._right_click_up

    def wheel(self):
        return self._wheel

    def wheel_change(self):
        return self._wheel_change

    def get_position(self):
        return self._position
    
    def _update_clicks(self):
        self._left_click = pygame.mouse.get_pressed()[0]
        self._wheel_click = pygame.mouse.get_pressed()[1]
        self._right_click = pygame.mouse.get_pressed()[2]

class Keyboard:
    def __init__(self):
        self._keys_state = dict()
        self._keys_down = dict()
        self._keys_up = dict()
    
    def update(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            name = pygame.key.name(event.key)

            self._keys_state[name] = True
            self._keys_down[name] = True
        elif event.type == pygame.KEYUP:
            name = pygame.key.name(event.key)

            self._keys_state[name] = False
            self._keys_up[name] = True
    
    def clear(self):
        self._keys_down.clear()
        self._keys_up.clear()
    
    def key_down(self, key_name: str):
        return self._keys_down.get(key_name, False)
    
    def key_up(self, key_name: str):
        return self._keys_up.get(key_name, False)
    
    def __getitem__(self, key_name: str):
        return self._keys_state.get(key_name, False)
