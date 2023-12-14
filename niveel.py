import pygame
from ajustes import screen_width,screen_height
from game_data import niveles

class Nivel():
    def __init__(self,nivel_actual,surface,crear_mundoexterior):
        #nivel setup
        self.display_surface = surface
        self.nivel_actual = nivel_actual
        nivel_data = niveles[nivel_actual]
        nivel_contenido = nivel_data['contenido']
        self.nuevo_nivel_max = nivel_data['desbloquear']
        self.crear_mundoexterior = crear_mundoexterior
        #Display de nivel
        self.fuente = pygame.font.Font(None,40)
        self.texto_surface = self.fuente.render(nivel_contenido,True,'white')
        self.texto_rect = self.texto_surface.get_rect(center = (screen_width / 2,screen_height / 2))
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.crear_mundoexterior(self.nivel_actual,self.nuevo_nivel_max)
        if keys[pygame.K_ESCAPE]:
            self.crear_mundoexterior(self.nivel_actual,0)
    def play(self):
        self.input()
        self.display_surface.blit(self.texto_surface,self.texto_rect)