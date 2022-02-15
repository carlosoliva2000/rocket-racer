import pygame as pygame
from Entorno import Entorno

pygame.init()  # Inicialización de la librería
clock = pygame.time.Clock()  # Reloj para mantener FPS estable
window = pygame.display.set_mode((1000, 500))
entorno = Entorno()

while True:
    clock.tick(1)
    accion = 0
    entorno.step(accion)
    entorno.render(window)
    pygame.display.update()
