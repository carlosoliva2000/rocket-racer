import numpy as np


class Entorno:
    COLOR = (50, 50, 50)

    def dibujar(self, ventana):
        ventana.fill(self.COLOR)


class Cohete:
    VEL_MAX = 5
    VEL_ROT = 0.1
    ACELERACION = 0.5  # Aceleración lineal
    RAYOS = 7  # Número de rayos para realizar el raycast
    COLOR = (255, 255, 255)

    def __init__(self):
        self.x = 500
        self.y = 250
        self.ang = 0  # Ángulo en radianes

        self.dx = 0
        self.dy = 0

    def mover(self, accion):
        # Actualizar variables de aceleración y rotación
        self.rotar(accion[1])
        self.acelerar(accion[0])

        self.x += self.dx
        self.y += self.dy

    def acelerar(self, aceleracion):
        self.dx += self.ACELERACION * aceleracion * np.cos(self.ang)
        self.dy += self.ACELERACION * aceleracion * np.sin(self.ang)

    def rotar(self, rotacion):
        self.ang -= self.VEL_ROT * rotacion

        # PENDIENTE MODIFICAR PARA QUE ESTÉ ENTRE 0 Y 2PI
        if self.ang > np.pi:
            self.ang = self.ang - 2 * np.pi
        if self.ang < -np.pi:
            self.ang = self.ang + 2 * np.pi

    def dibujar(self, ventana):
        import pygame
        from pygame import gfxdraw

        # Cohete sin antiliasing
        """
        pygame.draw.circle(ventana, self.COLOR, (self.x, self.y), 5.0)
        pygame.draw.line(ventana, self.COLOR, (self.x, self.y), (self.x + np.cos(self.ang) * 10,
                                                                 self.y + np.sin(self.ang) * 10))
        """

        # Cohete con antialiasing
        pygame.gfxdraw.aacircle(ventana, int(self.x), int(self.y), 5, self.COLOR)
        pygame.gfxdraw.filled_circle(ventana, int(self.x), int(self.y), 5, self.COLOR)
        pygame.draw.aaline(ventana, self.COLOR, (self.x, self.y), (self.x + np.cos(self.ang) * 10,
                                                                   self.y + np.sin(self.ang) * 10))
        # pygame.gfxdraw.aaline(ventana, int(self.x), int(self.y), int(self.x + np.cos(self.ang) * 10),
        #                    int(self.y + np.sin(self.ang) * 10), self.COLOR)

        # self.x = np.random.randint(0, ventana.get_width())
        # self.y = np.random.randint(0, ventana.get_height())
        # self.ang = np.random.rand() * 2 * np.pi

        # self.ang = np.deg2rad(np.random.randint(0, 360))
        # print(self.ang)


import pygame


def manejar_eventos(eventos):
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return True


def manejar_entrada(teclas):
    accion_acelerar = 0
    accion_rotar = 0
    if teclas[82]:  # K_up
        accion_acelerar = 1
    if teclas[81]:  # K_down
        accion_acelerar = -1
    if teclas[80]:  # K_left
        accion_rotar = 1
    if teclas[79]:  # K_right
        accion_rotar = -1
    return [accion_acelerar, accion_rotar]


pygame.init()
clock = pygame.time.Clock()  # Reloj para mantener FPS estable
ventana = pygame.display.set_mode((1000, 500))
entorno = Entorno()
cohete = Cohete()

entorno.dibujar(ventana)
while True:
    if manejar_eventos(pygame.event.get()):
        break

    input_teclado = list(pygame.key.get_pressed())
    cohete.mover(manejar_entrada(input_teclado))
    entorno.dibujar(ventana)
    cohete.dibujar(ventana)
    pygame.display.update()
    clock.tick(30)
