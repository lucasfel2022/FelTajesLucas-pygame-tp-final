from typing import Any
import pygame
from game_data import niveles
from soporte import *
class Nodo(pygame.sprite.Sprite):
    def __init__(self, pos, estado, icono_speed,path):
        super().__init__()
        self.frames = importar_folder(path)
        self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.Surface((100, 80))
        if estado == 'disponible':
            self.estado = 'disponible'
        else:
            self.estado = 'bloqueado'
        self.rect = self.image.get_rect(center=pos)
        self.zona_de_deteccion = pygame.Rect(
            self.rect.centerx - (icono_speed / 2),
            self.rect.centery - (icono_speed / 2),
            icono_speed, icono_speed
        )
    def animar(self):
         self.frame_index += 0.15
         if self.frame_index >= len(self.frames):
            self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]    
    def update(self):
        if self.estado =='disponible':
            self.animar()
        
class Icono(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('C:\\Juego_Labo\\start_game\\Jugador\\sombrero.png')
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos

class Mundo_exterior():
    def __init__(self, nivel_inicial, nivel_final, surface,crear_nivel):
        # setup
        self.display_surface = surface
        self.nivel_final = nivel_final
        self.nivel_actual = nivel_inicial
        self.crear_nivel = crear_nivel
        # Logica de mivimiento
        self.moviendo = False
        self.movimiento_direccion = pygame.math.Vector2(0, 0)
        self.speed = 8
        # sprites
        self.setup_nodos()
        self.setup_icono()

    def setup_nodos(self):
        self.nodos = pygame.sprite.Group()

        for indice, nodo_data in enumerate(niveles.values()):
            if indice <= self.nivel_final:
                nodo_sprite = Nodo(nodo_data['nodo_pos'], 'disponible', self.speed,nodo_data['nodo_graficos'])
                self.nodos.add(nodo_sprite)
            else:
                nodo_sprite = Nodo(nodo_data['nodo_pos'], 'bloqueado', self.speed,nodo_data['nodo_graficos'])
                self.nodos.add(nodo_sprite)

    def dibujar_paths(self):
        puntos = [nodo['nodo_pos'] for indice, nodo in enumerate(niveles.values()) if indice <= self.nivel_final]
        pygame.draw.lines(self.display_surface, '#a04f45', False, puntos, 6)

    def setup_icono(self):
        self.icono = pygame.sprite.GroupSingle()
        icono_sprite = Icono(self.nodos.sprites()[self.nivel_actual].rect.center)
        self.icono.add(icono_sprite)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moviendo:
            if keys[pygame.K_RIGHT] and self.nivel_actual < self.nivel_final:
                self.movimiento_direccion = self.get_data_movimiento('siguiente')
                self.nivel_actual += 1
                self.moviendo = True
            elif keys[pygame.K_LEFT] and self.nivel_actual > 0:
                self.movimiento_direccion = self.get_data_movimiento('anterior')
                self.nivel_actual -= 1
                self.moviendo = True
            elif keys[pygame.K_SPACE]:
                self.crear_nivel(self.nivel_actual)
                
    def icono_pos_update(self):
     if self.moviendo and self.movimiento_direccion:
        self.icono.sprite.pos += self.movimiento_direccion * self.speed
        objetivo_nodo = self.nodos.sprites()[self.nivel_actual]
        if objetivo_nodo.zona_de_deteccion.collidepoint(self.icono.sprite.pos):
            self.moviendo = False
            self.movimiento_direccion = pygame.math.Vector2(0, 0)

    def get_data_movimiento(self, objetivo):
        inicio = pygame.math.Vector2(self.nodos.sprites()[self.nivel_actual].rect.center)
        if objetivo == 'siguiente':
            fin = pygame.math.Vector2(self.nodos.sprites()[self.nivel_actual + 1].rect.center)
        else:
            fin = pygame.math.Vector2(self.nodos.sprites()[self.nivel_actual - 1].rect.center)
        return (fin - inicio).normalize()

    def play(self):
        self.dibujar_paths()
        self.icono_pos_update()
        self.icono.update()
        self.nodos.update()
        
        self.input()
        self.nodos.draw(self.display_surface)
        self.icono.draw(self.display_surface)