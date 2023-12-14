import pygame

# La clase GUI es responsable de configurar y mostrar varios elementos como la barra de salud y las
# monedas en la interfaz de un juego.
class GUI:
    def __init__(self,surface):
        """
        La función inicializa la superficie de visualización y carga imágenes para la barra de salud y
        las monedas.
        
        :param surface: El parámetro "superficie" es la superficie de visualización en la que se
        dibujarán los elementos de la interfaz de usuario. Suele ser un objeto Surface de pygame que
        representa la ventana o pantalla del juego
        """
        #setup
        self.display_surface = surface
        
        #Vida
        self.vida_barra = pygame.image.load('C:\\Juego_Labo\\start_game\\Jugador\\propiedades_nivel\\ui\\vida_barra.png')
        self.vida_barra_topleft = (54,39)
        self.barra_max_width = 152
        self.barra_height = 4
        #Monedas
        self.monedas = pygame.image.load('C:\\Juego_Labo\\start_game\\Jugador\\propiedades_nivel\\ui\\monedas.png')
        self.monedas_rect = self.monedas.get_rect(topleft = (50,61))
        self.fuente = pygame.font.Font('C:\\Juego_Labo\\start_game\\Jugador\\propiedades_nivel\\ui\\ARCADEPI.ttf',30)
        
    def mostrar_vida(self,actual,lleno):
        """
        La función "mostrar_vida" muestra una barra de salud en una superficie de pygame basada en los
        valores de salud actuales y máximos.
        
        :param actual: El valor actual de la salud o la vida
        :param lleno: El parámetro "lleno" representa el valor máximo de la barra de salud o vida. Es el
        valor que representa la salud o vida total o máxima del personaje u objeto
        """
        self.display_surface.blit(self.vida_barra,(20,10))
        ratio_de_salud_actual = actual / lleno
        barra_actual_width = self.barra_max_width * ratio_de_salud_actual
        barra_vida_rect = pygame.Rect((self.vida_barra_topleft),(barra_actual_width,self.barra_height))
        pygame.draw.rect(self.display_surface,'#dc4949',barra_vida_rect)
    def mostrar_monedas(self,cantidad):
        """
        La función muestra la cantidad de monedas en la pantalla.
        
        :param cantidad: El parámetro "cantidad" representa la cantidad de monedas que se mostrarán
        """
        self.display_surface.blit(self.monedas,self.monedas_rect)
        monedas_cantidad_surf = self.fuente.render(str(cantidad),False,'#33323d')
        monedas_cantidad_rect = monedas_cantidad_surf.get_rect(midleft = (self.monedas_rect.right + 4,self.monedas_rect.centery))
        self.display_surface.blit(monedas_cantidad_surf,monedas_cantidad_rect)