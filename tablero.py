# La variable `level_map` es una lista de cadenas que representa un mapa o diseño para un nivel de
# juego. Cada cadena de la lista representa una fila del mapa y cada carácter de la cadena representa
# un mosaico u objeto en esa fila. El mapa se compone de espacios vacíos (' '), paredes ('X') y un
# personaje jugador ('P'). El mapa se utiliza para determinar el diseño y los obstáculos en el nivel
# del juego.
import pygame
level_map = [
'                            ',
'                            ',
'                            ',
' XX    XXX            XX    ',
' XX P                       ',
' XXXX         XX         XX ',
' XXXX       XX              ',
' XX    X  XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

piso_tamaño = 64
screen_width = 1200
screen_height = len(level_map) * piso_tamaño



class Losas(pygame.sprite.Sprite):
	def __init__(self,pos,size):
		super().__init__()
		self.image = pygame.Surface((size,size))
		# `self.image.fill('grey')` está llenando la superficie del objeto con el color gris.
		self.image.fill("grey")
		self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift):
		self.rect.x += x_shift