import pygame
from tejas import AnimarTeja
from random import randint

class Enemigo(AnimarTeja):
    def __init__(self, size, x, y):
        try:
            super().__init__(size, x, y, 'C:\\Juego_Labo\\start_game\\enemy\\run')
            # Ajusta la coordenada y del rectángulo del enemigo
            self.rect.y += size - self.image.get_size()[1]
            # Asigna un valor entero aleatorio entre 3 y 5 a la velocidad del enemigo
            self.speed = randint(3, 5)
        except Exception as e:
            # Maneja la excepción, por ejemplo, imprimir un mensaje de error
            print(f"Error en la inicialización de Enemigo: {e}")

    def mover(self):
        try:
            # Mueve al enemigo horizontalmente
            self.rect.x += self.speed
        except Exception as e:
            # Maneja la excepción, por ejemplo, imprimir un mensaje de error
            print(f"Error en la función mover de Enemigo: {e}")

    def reversa(self):
        try:
            # Invierte la velocidad y voltea la imagen horizontalmente
            self.speed *= -1
            self.image = pygame.transform.flip(self.image, True, False)
        except Exception as e:
            # Maneja la excepción, por ejemplo, imprimir un mensaje de error
            print(f"Error en la función reversa de Enemigo: {e}")

    def update(self, shift):
        try:
            # Actualiza la coordenada x del rectángulo para seguir el desplazamiento de la pantalla
            self.rect.x += shift
            self.Animar()
            self.mover()
            self.reversa()
        except Exception as e:
            # Maneja la excepción, por ejemplo, imprimir un mensaje de error
            print(f"Error en la función update de Enemigo: {e}")
