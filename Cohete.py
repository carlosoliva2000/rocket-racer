import numpy as np


class Entorno:
    COLOR = (50, 50, 50)

    def dibujar(self, ventana):
        ventana.fill(self.COLOR)


class Cohete:
    VEL_MAX = 5
    VEL_ROT = 0.05
    ACELERACION = 0.5  # Aceleración lineal
    RAYOS = 7  # Número de rayos para realizar el raycast
    COLOR = (255, 255, 255)

    def __init__(self):
        self.x = 500
        self.y = 250
        self.ang = 0  # Ángulo en radianes

    def acelerar(self, aceleracion):
        pass

    def rotar(self, rotacion):
        pass

    def dibujar(self, ventana):
        import pygame
        pygame.draw.circle(ventana, self.COLOR, (self.x, self.y), 5.0)
        pygame.draw.line(ventana, self.COLOR, (self.x, self.y), (self.x+np.cos(self.ang)*10,
                                                                 self.y+np.sin(self.ang)*10))
        self.x = np.random.randint(0, ventana.get_width())
        self.y = np.random.randint(0, ventana.get_height())
        self.ang = np.random.rand()*2*np.pi
        # self.ang = np.deg2rad(np.random.randint(0, 360))
        # print(self.ang)


import pygame

pygame.init()
clock = pygame.time.Clock()  # Reloj para mantener FPS estable
ventana = pygame.display.set_mode((1000, 500))
entorno = Entorno()
cohete = Cohete()

while True:
    entorno.dibujar(ventana)
    cohete.dibujar(ventana)
    pygame.display.update()
    clock.tick(1)
