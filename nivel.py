# La clase "Nivel" representa un nivel en un juego y maneja la configuración, detección de colisiones
# y representación de varios elementos del juego, como terreno, monedas, enemigos y el personaje del
# jugador.
import pygame
from soporte import *
from ajustes import *
from tejas import *
from enemigo import *
from player import *
from efectos import *
from game_data import *
class Nivel():
    def __init__(self,nivel_actual,surface,crear_mundoexterior,cambiar_monedas,cambiar_vida):
        self.display_surface = surface
        self.cambio_mundo = 0
        
        #Audio
        self.moneda_sonido = pygame.mixer.Sound('C:\\Juego_Labo\\start_game\\Musica\\moneda.wav')
        
        
        #MundoExterno
        self.crear_mundoexterior = crear_mundoexterior
        self.nivel_actual = nivel_actual
        nivel_data = niveles[self.nivel_actual]
        self.nuevo_nivel_max = nivel_data['desbloquear']
        
        #Player
        player_diseño = importar_csv_diseño(nivel_data['jugador'])
        self.jugador_sprite = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        
        self.particula_sprite = pygame.sprite.GroupSingle()
        #explocion de particulas
        self.explocion_sprites = pygame.sprite.Group()
        self.jugador_setup(player_diseño,cambiar_vida)
        #Interfaz de Usuario
        self.cambiar_monedas = cambiar_monedas
        #Importar diseño del mapa
        diseño_terreno = importar_csv_diseño(nivel_data['Mapa'])
        self.terreno_sprites = self.crear_grupo_azulejos(diseño_terreno,'Mapa')
        #Importar diseño de 
        diseño_coins = importar_csv_diseño(nivel_data['monedas'])
        self.monedas_sprites = self.crear_grupo_azulejos(diseño_coins,'monedas')
        #Enemigos
        enemigo_diseño = importar_csv_diseño(nivel_data['Enemigos'])
        self.enemigos_sprites = self.crear_grupo_azulejos(enemigo_diseño,'Enemigos')
        limites_diseño = importar_csv_diseño(nivel_data['Limites'])
        self.limites_sprites = self.crear_grupo_azulejos(limites_diseño,'Limites') 
        #Corazones
        corazon_diseño = importar_csv_diseño(nivel_data['corazon'])
        self.corazon_sprites = self.crear_grupo_azulejos(corazon_diseño,'corazon')
        
        
    def crear_grupo_azulejos(self, disposicion, tipo):
            sprite_group = pygame.sprite.Group()
            for row_index, row in enumerate(disposicion):
                for col_index, val in enumerate(row):
                    sprite = None
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if val != '-1':
                        if tipo == 'Mapa':
                            terreno_lista = importar_graficos('C:\\Juego_Labo\\start_game\\Level\\Game\\plataforma.png')
                            teja_surface = terreno_lista[int(val)]
                            sprite = TejaEstatica(tile_size, x, y, teja_surface)

                    if val != '-1':
                        if tipo == 'monedas':
                            sprite = Moneda(tile_size, x, y, 'C:\\Juego_Labo\\start_game\\Level\\Game\\gold',5)
                        elif tipo == 'Enemigos':
                            sprite = Enemigo(tile_size, x, y)
                        elif tipo == 'Limites':
                            sprite = Teja(tile_size, x, y)
                    if sprite is not None:
                        sprite_group.add(sprite)
        
            return sprite_group
    def jugador_setup(self, disposicion,cambiar_vida):
        """
        La función "jugador_setup" configura el jugador y los sprites de objetivo en función de una
        disposición determinada y puede cambiar la vida del jugador.
        
        :param disposicion: El parámetro "disposición" es una lista 2D que representa la disposición de
        las fichas del juego. Cada elemento de la lista representa una ficha del juego y el valor del
        elemento determina el tipo de ficha
        :param cambiar_vida: Es probable que el parámetro "cambiar_vida" sea una función que se pasa a la
        clase "Jugador". Se utiliza para cambiar la vida o la salud del jugador de alguna manera"""
        try:
            for row_index, row in enumerate(disposicion):
                for col_index, val in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if val == '0':
                        sprite = Jugador((x, y), self.display_surface, self.crear_particulas_de_salto, cambiar_vida)
                        self.jugador_sprite.add(sprite)
                    if val == '-1':
                        sombrero_superficie = pygame.image.load('C:\\Juego_Labo\\start_game\\Jugador\\sombrero.png').convert_alpha()
                        sprite = TejaEstatica(tile_size, x, y, sombrero_superficie)
                        self.goal.add(sprite)
        except Exception as e:
        # Manejar la excepción, por ejemplo, imprimir un mensaje de error
            print(f"Error en jugador_setup: {e}")
            
    def colision_movimiento_horizontal(self):
        """
        La función maneja la detección de colisiones y el movimiento de un objeto de jugador en
        dirección horizontal.
        """
        try:
            jugador = self.jugador_sprite.sprite
            jugador.rect.x += jugador.direccion.x * jugador.speed
            sprites_colisionables = self.terreno_sprites.sprites() 

            for sprite in sprites_colisionables:
                if sprite.rect.colliderect(jugador.rect):
                    if jugador.direccion.x < 0: 
                        jugador.rect.left = sprite.rect.right
                        jugador.en_izquierda = True
                    elif jugador.direccion.x > 0:
                        jugador.rect.right = sprite.rect.left
                        jugador.en_derecha = True

            if jugador.en_izquierda and jugador.direccion.x >= 0:
                jugador.en_izquierda = False
            if jugador.en_derecha and jugador.direccion.x <= 0:
                jugador.en_derecha = False
    
        except Exception as e:
        # Manejar la excepción, por ejemplo, imprimir un mensaje de error
            print(f"Error en colision_movimiento_horizontal: {e}")

    def colision_movimiento_vertical(self):
        """
        La función comprueba si hay colisiones verticales entre el jugador y los sprites del terreno y
        ajusta la posición y velocidad del jugador en consecuencia.
        """
        try:
            jugador = self.jugador_sprite.sprite
            jugador.aplicar_gravedad()
            sprites_colisionables = self.terreno_sprites.sprites()

            for sprite in sprites_colisionables:
                if sprite.rect.colliderect(jugador.rect):
                    if jugador.direccion.y > 0: 
                        jugador.rect.bottom = sprite.rect.top
                        jugador.direccion.y = 0
                        jugador.en_tierra = True
                    elif jugador.direccion.y < 0:
                        jugador.rect.top = sprite.rect.bottom
                        jugador.direccion.y = 0
                        jugador.en_techo = True

            if jugador.en_tierra and jugador.direccion.y < 0 or jugador.direccion.y > 1:
                jugador.en_tierra = False
            if jugador.en_techo and jugador.direccion.y > 0.1:
                jugador.en_techo = False
    
        except Exception as e:
        # Manejar la excepción, por ejemplo, imprimir un mensaje de error
          print(f"Error en colision_movimiento_vertical: {e}")     
    def colision_en_reversa(self):
        try:
            for enemigo in self.enemigos_sprites.sprites():
                if pygame.sprite.spritecollide(enemigo, self.limites_sprites, False):
                    enemigo.reversa()
        except Exception as e:
            print(f"Error en colision_en_reversa: {e}")

    def crear_particulas_de_salto(self, pos):
        try:
            jugador = self.jugador_sprite.sprite
            if jugador.frente_derecho:
                pos -= pygame.math.Vector2(10, 5)
            else:
                pos += pygame.math.Vector2(10, -5)
            salto_sprite = ParticulasEfectos(pos, 'jump')
            self.particula_sprite.add(salto_sprite)
        except Exception as e:
         print(f"Error en crear_particulas_de_salto: {e}")

    def scroll_x(self):
        try:
            jugador = self.jugador_sprite.sprite
            jugador_x = jugador.rect.centerx
            direccion_x = jugador.direccion.x
            if jugador_x < screen_width / 4 and direccion_x < 0:
                self.cambio_mundo = 8
                jugador.speed = 0
            elif jugador_x > screen_width - (screen_width / 4) and direccion_x > 0:
                self.cambio_mundo = -8
                jugador.speed = 0
            else:
                self.cambio_mundo = 0
                jugador.speed = 8
        except Exception as e:
            print(f"Error en scroll_x: {e}")

    def chequear_muerte(self):
        try:
            if self.jugador_sprite.sprite.rect.top > screen_height:
                self.crear_mundoexterior(self.nivel_actual, 0)
        except Exception as e:
            print(f"Error en chequear_muerte: {e}")

    def chequear_nivel_pased(self):
        try:
            if pygame.sprite.spritecollide(self.jugador_sprite.sprite, self.goal, False):
                self.crear_mundoexterior(self.nivel_actual, self.nuevo_nivel_max)
        except Exception as e:
            print(f"Error en chequear_nivel_pased: {e}")

    def chequear_colision_monedas(self):
        try:
            monedas_colisionadas = pygame.sprite.spritecollide(self.jugador_sprite.sprite, self.monedas_sprites, True)
            if monedas_colisionadas:
                self.moneda_sonido.play()
                for moneda in monedas_colisionadas:
                    self.cambiar_monedas(moneda.valor)
        except Exception as e:
            print(f"Error en chequear_colision_monedas: {e}")

    def chequear_colision_enemigo(self):
        try:
            enemigo_colisiones = pygame.sprite.spritecollide(self.jugador_sprite.sprite, self.enemigos_sprites, False)
            if enemigo_colisiones:
                for enemigo in enemigo_colisiones:
                    enemigo_center = enemigo.rect.centery
                    enemigo_top = enemigo.rect.top
                    jugador_boton = self.jugador_sprite.sprite.rect.bottom
                    if enemigo_top < jugador_boton < enemigo_center and self.jugador_sprite.sprite.direccion.y >= 0:
                        self.jugador_sprite.sprite.direccion.y = -15
                        explocion_sprite = ParticulasEfectos(enemigo.rect.center, 'explocion')
                        self.explocion_sprites.add(explocion_sprite)
                        enemigo.kill()
                    else:
                        self.jugador_sprite.sprite.get_daño()
        except Exception as e:
            print(f"Error en chequear_colision_enemigo: {e}")
        
    def play(self):
        self.terreno_sprites.update(self.cambio_mundo)
        self.terreno_sprites.draw(self.display_surface)
        
        #monedas
        self.monedas_sprites.update(self.cambio_mundo)
        self.monedas_sprites.draw(self.display_surface)
        #enemigos
        #self.enemigos_sprites.update(self.cambio_mundo)
        #self.enemigos_sprites.draw(self.display_surface)
        #self.explocion_sprites.update(self.cambio_mundo)
        #self.explocion_sprites.draw(self.display_surface)
        #limites
        self.limites_sprites.update(self.cambio_mundo)
        self.colision_en_reversa()
        self.colision_movimiento_horizontal()
        self.colision_movimiento_vertical()
        #corazon
        self.corazon_sprites.update(self.cambio_mundo)
        self.corazon_sprites.draw(self.display_surface)
        #Jugador
        self.jugador_sprite.update()
        self.jugador_sprite.draw(self.display_surface)
        self.goal.update(self.cambio_mundo)
        self.goal.draw(self.display_surface)
        
        self.scroll_x()
        
        self.chequear_muerte()
        self.chequear_nivel_pased()
        #self.chequear_colision_enemigo()
        self.chequear_colision_monedas()