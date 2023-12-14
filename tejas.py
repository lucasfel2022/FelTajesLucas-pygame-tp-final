import pygame
from soporte import *
class Teja(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift
        
class TejaEstatica(Teja):
    def __init__(self, size, x, y,surface):
        super().__init__(size, x, y)
        self.image = surface
        
class AnimarTeja(Teja):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = importar_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index] 
  
    def Animar(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    def update(self, shift):
        self.Animar()
        self.rect.x += shift
class Moneda(AnimarTeja):
    def __init__(self, size, x, y, path, valor):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.valor = valor