import pygame.image

path = "datas/textures/gui/"

main_background = pygame.image.load("datas/textures/backgrounds/main.png")
pygame.display.set_icon(main_background)

search = pygame.image.load("datas/textures/gui/search/24x24.png")
search_hover = pygame.image.load("datas/textures/gui/search_hover/24x24.png")

add_button = pygame.image.load("datas/textures/gui/add_button/22x22.png")
add_hover_button = pygame.image.load("datas/textures/gui/add_button_hover/22x22.png")

close_button = pygame.image.load("datas/textures/gui/close_button/12x12.png")
close_hover_button = pygame.image.load("datas/textures/gui/close_button_hover/12x12.png")

arrow_right = pygame.image.load("datas/textures/gui/arrow/20x20.png")
arrow_hover_right = pygame.image.load("datas/textures/gui/arrow_hover/20x20.png")

arrow_up = pygame.transform.rotate(arrow_right, 90)
arrow_hover_up = pygame.transform.rotate(arrow_hover_right, 90)

arrow_left = pygame.transform.rotate(arrow_up, 90)
arrow_hover_left = pygame.transform.rotate(arrow_hover_up, 90)

arrow_down = pygame.transform.rotate(arrow_left, 90)
arrow_hover_down = pygame.transform.rotate(arrow_hover_left, 90)