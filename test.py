import pygame, sys
pygame.init()
mille=1000

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
pikmin = pygame.image.load('pikman2.png').convert()
background = pygame.image.load('bg.jpg').convert()
screen.blit(background, (0, 0))
groupe = pygame.sprite.RenderClear()

class Objtest(pygame.sprite.Sprite):
    
    def __init__(self, image:pygame.Surface, height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = image.get_rect().move(0, height)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.pos.right += self.speed
        if keys[pygame.K_DOWN]:
            self.pos.right -= self.speed
        if keys[pygame.K_LEFT]:
            self.pos.top += self.speed
        if keys[pygame.K_RIGHT]:
            self.pos.top -= self.speed

pikmin = Objtest(pikmin, 128, 1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    groupe.update()
    screen.blit(background, (0, 0))
    groupe.draw(screen)
    pygame.display.update()
    clock.tick(60)