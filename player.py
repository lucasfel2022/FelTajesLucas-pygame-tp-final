import pygame
from soporte import importar_folder
from math import sinh
class Jugador(pygame.sprite.Sprite):
    def __init__(self,pos,surface,crear_particulas_de_salto,cambiar_vida):
        super().__init__()
        self.importar_caracter_assets()
        
        self.frame_index = 0
        self.animacion_speed = 0.15
        self.image = self.animaciones['Stand'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        # `self.direccion = pygame.math.Vector2(0,0)` está inicializando el atributo `self.direccion`
        # de la clase `Jugador` con un objeto `Vector2` del módulo `pygame.math`.
        #Dust_particulas
        self.importar_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animacion_speed = 0.15
        self.display_surface = surface
        self.crear_particulas_de_salto = crear_particulas_de_salto
        self.direccion = pygame.math.Vector2(0,0)
        #Movimiento de jugador
        self.speed = 4
        self.gravedad = 0.8
        self.salto_velocidad = -16
        #Jugador Estados
        self.status = 'Stand'
        self.frente_derecho = True
        self.en_tierra = False
        self.en_techo = False
        self.en_izquierda = False
        self.en_derecha = False
        #Vida 
        self.cambiar_vida = cambiar_vida
        self.invensible = False
        self.invensibilidad_duracion = 400
        self.tiempo_daño = 0 
        #sonidos
        #self.salto_sonido = pygame.mixer.Sound('C:\\Juego_Labo\\start_game\\Musica\\salto')
        
        
    def importar_caracter_assets(self):  
        caracter_path ='C:\\Juego_Labo\\start_game\\viking_axe\\'
        self.animaciones = {'Stand':[],'Run':[],'Jump':[],'Hit':[]}
        
        for animacion in self.animaciones.keys():
            full_path = f"{caracter_path}\\{animacion}"  # Usa \\ o / para separar componentes
            self.animaciones[animacion] = importar_folder(full_path)
    
    def importar_dust_run_particles(self):
        self.dust_run_particles = importar_folder('C:\\Juego_Labo\\start_game\\images\\caracters\\dust_particles\\run')
            
    def run_dust_animacion(self):
        """
        La función `run_dust_animation` muestra una animación de partículas de polvo basada en el estado
        actual y la posición de un objeto.
        """
        if self.status == 'Run' and self.en_tierra:
            self.dust_frame_index += self.dust_animacion_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
                
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            
            if self.frente_derecho:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle,pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust_particle,pos) 
                
    def animar(self):
        animacion = self.animaciones[self.status]

        self.frame_index += self.animacion_speed
        if self.frame_index >= len(animacion):
            self.frame_index = 0
        self.image = animacion[int(self.frame_index)]
        if self.frente_derecho:
            self.image = self.image
        else:
            flipped_image = pygame.transform.flip(self.image,True,False)
            self.image = flipped_image

        if self.en_tierra and self.en_derecha:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.en_tierra and self.en_izquierda:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)   
        elif self.en_tierra:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        if self.en_techo and self.en_derecha:
            self.rect = self.image.get_rect(topright = self.rect.bottomright)
        elif self.en_techo and self.en_izquierda:
            self.rect = self.image.get_rect(topleft = self.rect.bottomleft)   
        elif self.en_techo:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
    def obtener_entrada(self):
        """
        La función verifica las entradas del teclado, establece la dirección del movimiento y realiza un
        salto si se presiona la tecla espacio.
        """
        try:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.direccion.x = 1
                self.frente_derecho = True
            elif keys[pygame.K_LEFT]:
                self.direccion.x = -1
                self.frente_derecho = False
            else:
                self.direccion.x = 0

            if keys[pygame.K_SPACE] and self.en_tierra:
                self.salto()
                self.crear_particulas_de_salto(self.rect.midbottom)
    
        except Exception as e:
            # Manejar la excepción, por ejemplo, imprimir un mensaje de error
            print(f"Error en obtener_entrada: {e}")
    def obtener_estado(self):
       if self.direccion.y < 0:
           self.status = 'Jump'
       else:
           if self.direccion.x != 0:
               self.status = 'Run'
           else:
               self.status = 'Stand'    
       
     
    def aplicar_gravedad(self):
        """
        La función aplica gravedad a la coordenada y de un objeto y actualiza su posición.
        """
        self.direccion.y += self.gravedad
        self.rect.y += self.direccion.y
        
    def salto(self):
        """
        La función "saltar" actualiza la coordenada y del atributo "dirección" al valor de
        "jump_velocity".
        """
        self.direccion.y  = self.salto_velocidad
        #self.salto_sonido.play()
    
    def get_daño(self):
        if not self.invensible:
            self.cambiar_vida(-10)
            self.invensible = True
            self.tiempo_daño = pygame.time.get_ticks()
    def invensibilidad_tiempo(self):
        try:
            tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual en milisegundos
            if tiempo_actual - self.tiempo_daño >= self.invensibilidad_duracion:
                self.invensible = False
        except Exception as e:
            print(f"Error en invensibilidad_tiempo: {e}")
    def update(self):
        """
        La función "actualizar" llama al método "obtener_entrada" para actualizar el objeto.
        """
        self.obtener_entrada()
        self.obtener_estado()
        self.animar()
        self.run_dust_animacion()
        self.invensibilidad_tiempo()
       