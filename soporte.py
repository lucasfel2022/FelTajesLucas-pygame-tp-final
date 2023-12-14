from csv import reader
from ajustes import *
import pygame
from os import walk
# La línea "from os import walk" importa la función "walk" del módulo "os". La función `walk` se
# utiliza para generar los nombres de los archivos en un árbol de directorios recorriendo el árbol de
# arriba hacia abajo o de abajo hacia arriba. En este código, se utiliza para iterar sobre todos los
# archivos en un directorio determinado.


def importar_folder(path):
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list



def importar_csv_diseño(path):
    terreno_map = []
    try:
        with open(path) as map:
            nivel = reader(map, delimiter=',')
            for row in nivel:
                terreno_map.append(list(row))
        return terreno_map
    except FileNotFoundError:
        print(f"Error: El archivo no se encuentra en la ruta especificada: {path}")
        return None
def importar_graficos(path):
    """
    La función importa gráficos de una ruta determinada, los corta en mosaicos y devuelve una lista de
    los mosaicos cortados.
    
    :param path: El parámetro de ruta es la ruta del archivo de imagen que contiene los gráficos que
    desea importar
    :return: una lista de mosaicos cortados, que son objetos pygame.Surface.
    """
    surface = pygame.image.load(path).convert_alpha()
    teja_num_x = int(surface.get_size()[0] / tile_size)
    teja_num_y = int(surface.get_size()[1] / tile_size)

    tejas_lista= []
    for row in range(teja_num_y):
        for col in range(teja_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size,tile_size),flags = pygame.SRCALPHA)
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
            tejas_lista.append(new_surf)
    return tejas_lista    
	