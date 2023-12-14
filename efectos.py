import pygame
from soporte import importar_folder

class ParticulasEfectos(pygame.sprite.Sprite):
	def __init__(self,pos,tipo):
		super().__init__()
		self.frame_index = 0
		self.animacion_speed = 0.5
		if tipo == 'jump':
			self.frames = importar_folder('C:\\Juego_Labo\\start_game\\images\\caracters\\dust_particles\\jump')
		if tipo == 'land':
			self.frames = importar_folder('C:\\Juego_Labo\\start_game\\images\\caracters\\dust_particles\\land')
		if tipo == 'explosion':
			self.frames = importar_folder('C:\\Juego_Labo\\start_game\\images\\caracters\\dust_particles\\explocion')
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.animacion_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift
