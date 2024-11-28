import pygame
import os

def load_images(images_path="assets/images", cell_size=80):
    """
    Carga y devuelve un diccionario con las imágenes escaladas al tamaño de las celdas.

    Args:
        images_path (str): Ruta al directorio donde están las imágenes.
        cell_size (int): Tamaño de las celdas del tablero.

    Returns:
        dict: Diccionario donde las claves son los identificadores de las piezas (e.g., "E1") 
              y los valores son las imágenes cargadas y escaladas.
    """
    images = {}
    try:
        images = {
            "E1": pygame.image.load(os.path.join(images_path, "elefante1.png")),
            "E2": pygame.image.load(os.path.join(images_path, "elefante2.png")),
            "C1": pygame.image.load(os.path.join(images_path, "camello1.png")),
            "C2": pygame.image.load(os.path.join(images_path, "camello2.png")),
            "H1": pygame.image.load(os.path.join(images_path, "caballo1.png")),
            "H2": pygame.image.load(os.path.join(images_path, "caballo2.png")),
            "D1": pygame.image.load(os.path.join(images_path, "perro1.png")),
            "D2": pygame.image.load(os.path.join(images_path, "perro2.png")),
            "R1": pygame.image.load(os.path.join(images_path, "conejo1.png")),
            "R2": pygame.image.load(os.path.join(images_path, "conejo2.png")),
        }

        # Escalar las imágenes al tamaño de las celdas
        for key, image in images.items():
            images[key] = pygame.transform.scale(image, (cell_size, cell_size))
    except pygame.error as e:
        print(f"Error al cargar las imágenes: {e}")

    return images