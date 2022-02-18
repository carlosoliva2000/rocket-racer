import sys
import gym
import numpy as np
import pygame
from pygame import gfxdraw


class Entorno:
    COLOR = (50, 50, 50)

    def __init__(self):
        """
        Llama a la función inicializar.
        """
        self.bordes1 = None
        self.bordes2 = None
        self.checkpoints = None
        self.inicializar()

    def inicializar(self):
        """
        Llama a la función generar_nivel, carga el número de checkpoints.
        """
        self.generar_nivel()

    def generar_nivel(self):
        """
        Genera el nivel aleatorio, primero generando segmentos y luego aplicándoles anchura, y checkpoints.
        """
        pass

    def mover(self):
        """
        Desplaza los elementos del entorno para que el jugador permanezca centrado.
        """
        pass

    def obtener_checkpoint_sig(self):
        """
        Dado el checkpoint actual, devuelve el siguiente.
        :return: checkpoint siguiente.
        """
        pass

    def obtener_checkpoint_ant(self):
        """
        Dado el checkpoint actual, devuelve el anterior.
        :return: checkpoint anterior.
        """
        pass

    def render(self, ventana):
        """
        Renderiza el entorno completo: paredes y checkpoints.
        """
        ventana.fill(self.COLOR)


class Cohete:
    # VEL_MAX = 5
    VEL_ROT = 0.1
    ACELERACION = 0.5  # Aceleración lineal
    RAYOS = 7  # Número de rayos para realizar el raycast
    COLOR = (255, 255, 255)

    def __init__(self, entorno, x=0, y=0):
        """
        Define el entorno y llama a inicializar.
        """
        self.entorno = entorno

        # Posición y orientación
        self.x = x
        self.y = y
        self.ang = 0  # Ángulo en radianes

        # Velocidad
        self.dx = 0
        self.dy = 0

        # Checkpoints
        self.checkpoint_actual = 0
        self.checkpoint_anterior = 0
        self.checkpoint_siguiente = 0

        # Recompensa
        self.recompensa = 0

        # Raycast
        self.raycast = None

        # self.inicializar()

    def inicializar(self, x=0):
        """
        Define posición, velocidad, checkpoints, recompensa y actualiza raycast.
        """
        self.x = x
        pass

    def actualizar(self, accion):
        """
        Rota, acelera y mueve, comprueba colisiones, actualiza el raycast, actualiza las observaciones y su recompensa.
        """
        self.mover(accion)

    def rotar(self, rotacion):
        """
        Rota el cohete y deja su angulo en [0, 2pi].
        """
        self.ang -= self.VEL_ROT * rotacion

        # PENDIENTE MODIFICAR PARA QUE ESTÉ ENTRE 0 Y 2PI
        if self.ang > np.pi:
            self.ang = self.ang - 2 * np.pi
        if self.ang < -np.pi:
            self.ang = self.ang + 2 * np.pi

    def acelerar(self, aceleracion):
        """
        Acelera el cohete (transforma su velocidad, no su posición).
        """
        self.dx += self.ACELERACION * aceleracion * np.cos(self.ang)
        self.dy += self.ACELERACION * aceleracion * np.sin(self.ang)

    def mover(self, accion):
        """
        Rota, acelera y mueve el cohete, generando vector movimiento.
        """
        # Actualizar variables de aceleración y rotación
        self.rotar(accion[1])
        self.acelerar(accion[0])

        self.x += self.dx
        self.y += self.dy

        # --------------------- VECTOR MOVIMIENTO -----------------------

    def comprobar_colision_checkpoints(self):
        """
        Detecta si se ha traspasado un checkpoint o si se ha retrocedido (mediante vector movimiento),
        actualizando su cp actual, el anterior y el siguiente.
        """
        pass

    def comprobar_colision_entorno(self):
        """
        Detecta si se ha colisionado con un elemento del entorno (mediante vector movimiento). Activa flag_colision.
        """
        pass

    def actualizar_raycast(self):
        """
        Actualiza cada rayo, colocándolo alrededor del cohete y definiendo su longitud.
        """
        pass

    def actualizar_observaciones(self):
        """
        Almacena en observaciones las distancias de los rayos y otras necesarias.
        """
        pass

    def actualizar_recompensa(self):
        """
        Almacena en recompensa los puntos obtenidos en esa actualización.
        """
        pass

    def interseccion(self):
        pass

    def render(self, ventana):
        """
        Renderiza el cohete
        """
        pygame.gfxdraw.aacircle(ventana, int(self.x), int(self.y), 5, self.COLOR)
        pygame.gfxdraw.filled_circle(ventana, int(self.x), int(self.y), 5, self.COLOR)
        pygame.draw.aaline(ventana, self.COLOR, (self.x, self.y), (self.x + np.cos(self.ang) * 10,
                                                                   self.y + np.sin(self.ang) * 10))


class Juego(gym.Env):
    def __init__(self, render=False):
        """
        Define action_space y observation_space. Contiene referencias a entorno y cohetes.
        Contiene ventana donde renderizar todo.
        """
        self.action_space = []
        self.observation_space = []

        self.entorno = Entorno()
        self.cohete = Cohete(self.entorno, 400, 300)

        # Atributos realizados con PyGame
        if not render:
            print("WARNING: Las opciones de renderizado no han sido activadas. Llamar a render() lanzará un error.\n"
                  "         Para activarlo, llame a inicializar_render().")
            self.clock = None
            self.ventana = None
        else:
            self.inicializar_render()

    def step(self, action):
        """
        Actualiza el cohete con su acción, comprueba estado colisión, obtiene las observaciones del cohete,
        obtiene las recompensas del cohete.
        :param action: acción que realiza el cohete.
        :return: o, r, d, i. (POR DEFINIR)
        """
        self.cohete.actualizar(action)

    def reset(self):
        pass

    def render(self, mode="human"):
        """
        Renderiza el entorno, los cohetes y gui.
        :param mode: POR DEFINIR.
        :return: POR DEFINIR.
        """

        # Limpiamos pantalla
        # self.ventana.fill((0, 0, 0))

        # Renderizamos el entorno
        self.entorno.render(self.ventana)

        # Renderizamos el cohete
        self.cohete.render(self.ventana)

        # Actualizamos la pantalla con el frame generado
        pygame.display.update()

    def inicializar_render(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.ventana = pygame.display.set_mode((800, 600))
