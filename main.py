import pygame,sys
from ajustes import *
from game_data import *
from Mundo_exterior import Mundo_exterior
from nivel import Nivel
from gui import *
#Nombre del Alumno: Lucas Agustin Fel Tajes
#Nombre del Juego: Aventuras de un Vikingo: El Camino de las Monedas
class Game():
    def __init__(self):
        #Atributos de juego
        self.nivel_final = 2
        self.vida_maxima = 100
        self.vida_actual = 100
        self.monedas = 0
        #Mundo Exterior
        self.mundo_exterior = Mundo_exterior(0,self.nivel_final,screen,self.crear_nivel)
        self.estado = 'mundoexterior'
        #Interfaz de Usuario
        self.gui = GUI(screen)
        #Audio nivel:
        self.nivel_music = pygame.mixer.Sound('C:\\Juego_Labo\\start_game\\Musica\\nivel_1.wav')
        self.mundoexterno_music = pygame.mixer.Sound('C:\\Juego_Labo\\start_game\\Musica\\niveles_set_up.wav')
        #self.nivel_music.play(loops=-1)
        
    def crear_nivel(self,nivel_actual):
        """
        La función "crear_nivel" crea un nuevo nivel en un juego y cambia el estado del juego a "nivel".
        
        :param nivel_actual: El parámetro "nivel_actual" representa el nivel actual del juego. Se utiliza
        para crear una nueva instancia de la clase "Nivel", pasando el nivel actual como argumento
        """
        self.nivel = Nivel(nivel_actual,screen,self.crear_mundoexterior,self.cambiar_monedas,self.cambiar_vida)
        self.estado = 'nivel'
        self.mundoexterno_music.stop()
        self.nivel_music.play(loops=-1)
        
    def crear_mundoexterior(self,nivel_actual,nuevo_nivel_max):
        if nuevo_nivel_max > self.nivel_final:
            self.nivel_final = nuevo_nivel_max
        else:
            self.nivel_final = nuevo_nivel_max
        self.mundoexterior = Mundo_exterior(nivel_actual,self.nivel_final, screen, self.crear_nivel)
        self.estado = 'mundoexterior'
        self.mundoexterno_music.play(loops=-1)
        self.nivel_music.stop()
    def cambiar_monedas(self,cantidad):
        self.monedas += cantidad
        
    def cambiar_vida(self,cantidad):
        self.vida_actual += cantidad
    def play(self):
        if self.estado == 'mundoexterior':
            self.mundo_exterior.play()
        else:
            self.nivel.play()
            self.gui.mostrar_vida(self.vida_actual,self.vida_maxima)
            self.gui.mostrar_monedas(self.monedas)
pygame.display.set_caption("Aventuras de un Vikingo: El Camino de las Monedas")
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.init()
clock = pygame.time.Clock()
FPS = 60
game = Game()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    delta_ms = 16
    screen.fill("grey")
    game.play()
    pygame.display.flip()
    pygame.display.update()                        
    delta_ms = clock.tick(FPS)