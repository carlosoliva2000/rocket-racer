import sys
import gym
import numpy as np
import pygame
from pygame import gfxdraw


class Entorno:
    COLOR = (50, 50, 50)

    def __init__(self, pos_inicial=(0, 0)):
        """
        Llama a la función inicializar.
        """
        self.recorrido = None
        self.bordes1 = None
        self.bordes2 = None
        self.checkpoints = None
        self.pos_inicial = pos_inicial
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
        longitud_min = 60
        longitud_max = 150
        d_ang = 0 # 0.5  # 0.8
        anchura_min = 50
        anchura_max = 150
        d_anchura = 5
        segmentos = 50

        # Recorrido es una matriz de 3 columnas que representan:
        # - [0] = x
        # - [1] = y
        # - [2] = ang
        recorrido = np.zeros((segmentos, 3))
        bordes1 = np.zeros((segmentos, 2))
        bordes2 = np.zeros((segmentos, 2))
        anchura = (anchura_min + anchura_max) // 2

        # Ajustamos los valores iniciales del recorrido
        # Es necesario empezar ligeramente a la derecha del cohete, ya que al final añadiremos dos puntos a cada lista
        # para cerrar el recorrido por la izquierda
        recorrido[0, 0] = self.pos_inicial[0] + 50
        recorrido[0, 1] = self.pos_inicial[1]
        bordes1[0, 0] = self.pos_inicial[0] + 50
        bordes1[0, 1] = self.pos_inicial[1]
        bordes2[0, 0] = self.pos_inicial[0] + 50
        bordes2[0, 1] = self.pos_inicial[1]

        for i in range(1, segmentos):
            # Longitud del segmento actual
            longitud = np.random.randint(longitud_min, longitud_max)

            # Sentido del giro del segmento
            signo = 1 if np.random.rand() > 0.5 else -1

            # Ángulo del nuevo segmento en función del anterior
            angulo = recorrido[i - 1, 2] + signo * np.random.rand() * d_ang
            # print(angulo)
            if angulo > np.pi:
                angulo -= 2 * np.pi
            if angulo < -np.pi:
                angulo += 2 * np.pi

            # Calculamos los puntos de destino del nuevo segmento
            x_ant, y_ant = recorrido[i - 1, 0], recorrido[i - 1, 1]
            x = x_ant + longitud * np.cos(angulo)
            y = y_ant + longitud * np.sin(angulo)

            # Comprobamos si existe colisión con el segmento anterior
            # En caso de producirse, retrocedemos N pasos o iteraciones
            ############################################################

            # Guardamos el recorrido en la matriz
            recorrido[i, 0] = x
            recorrido[i, 1] = y
            recorrido[i, 2] = angulo

            # Establece si la anchura crece o decrece en el segmento
            # signo = 1 if np.random.rand() > 0.5 else -1

            # Generamos anchura para el recorrido y sus respectivos bordes
            # anchura = np.clip(anchura_ant + signo * np.random.rand() * d_anchura, anchura_min, anchura_max)
            # print(anchura)
            # bordes1[i, 0] = x + anchura * np.cos(angulo + 0.5 * np.pi)
            # bordes1[i, 1] = y + anchura * np.sin(angulo + 0.5 * np.pi)
            # bordes2[i, 0] = x - anchura * np.cos(angulo + 0.5 * np.pi)
            # bordes2[i, 1] = y - anchura * np.sin(angulo + 0.5 * np.pi)

        i = 0
        while i < segmentos:
            # Establece si la anchura crece o decrece en el segmento
            if anchura == anchura_max:
                signo = -1
            elif anchura == anchura_min:
                signo = 1
            else:
                signo = 1 if np.random.rand() > 0.5 else -1

            j = 0
            while i < segmentos and j < np.random.randint(5, 15):
                # Generamos anchura para el recorrido en función de la anterior y lo limitamos
                anchura = np.clip(anchura + signo * np.random.rand() * d_anchura, anchura_min, anchura_max)
                # print(anchura)

                # Definimos los bordes a partir del recorrido y su anchura
                # Los nuevos puntos se definen tomando la perpendicular del segmento
                x = recorrido[i, 0]
                y = recorrido[i, 1]
                angulo = recorrido[i, 2]
                bordes1[i, 0] = x + anchura * np.cos(angulo + 0.5 * np.pi)
                bordes1[i, 1] = y + anchura * np.sin(angulo + 0.5 * np.pi)
                bordes2[i, 0] = x - anchura * np.cos(angulo + 0.5 * np.pi)
                bordes2[i, 1] = y - anchura * np.sin(angulo + 0.5 * np.pi)

                # Aumentamos contadores
                j += 1
                i += 1

                if anchura == anchura_max or anchura == anchura_min:
                    break

        # Ajustes para comenzar siempre hacia la derecha y recto
        borde1_inicio = np.array([[self.pos_inicial[0] - 100, self.pos_inicial[1]],
                                  [self.pos_inicial[0] - 50, self.pos_inicial[1] + 100]])
        borde2_inicio = np.array([[self.pos_inicial[0] - 100, self.pos_inicial[1]],
                                  [self.pos_inicial[0] - 50, self.pos_inicial[1] - 100]])
        recorrido_inicio = np.array([[self.pos_inicial[0] - 100, self.pos_inicial[1]],
                                     [self.pos_inicial[0] - 50, self.pos_inicial[1]]])
        # Concatenamos los inicios a las listas, y en el caso de recorrido, recortamos las columnas
        # para quedarnos solo con las posiciones x e y
        recorrido = np.concatenate([recorrido_inicio, recorrido[:, :2]])
        bordes1 = np.concatenate([borde1_inicio, bordes1], axis=0)
        bordes2 = np.concatenate([borde2_inicio, bordes2], axis=0)

        # Creamos los checkpoints como vectores que contienen los puntos en cada borde a lo largo de la pista
        checkpoints = np.zeros((segmentos, 4))
        checkpoints[:, [0, 1]] = np.copy(bordes1)[2:]
        checkpoints[:, [2, 3]] = np.copy(bordes2)[2:]

        self.recorrido = recorrido  # [:, :2]
        self.bordes1 = bordes1
        self.bordes2 = bordes2
        self.checkpoints = checkpoints

        print("---")
        print(self.checkpoints)
        print("---")

    def mover(self, dx, dy):
        """
        Desplaza los elementos del entorno para que el jugador permanezca centrado.
        """
        self.recorrido -= (dx, dy)
        self.bordes1 -= (dx, dy)
        self.bordes2 -= (dx, dy)
        self.checkpoints -= (dx, dy, dx, dy)  # Al tener 4 columnas, es necesario restar a todas ellas el dx y dy

    def obtener_checkpoint_sig(self, n_checkpoint=0):
        """
        Dado el checkpoint actual, devuelve el siguiente.
        :return: número de checkpoint siguiente y sus coordenadas.
        """
        if n_checkpoint+1 < len(self.checkpoints):
            return n_checkpoint+1, self.checkpoints[n_checkpoint+1]
        else:
            return n_checkpoint, self.checkpoints[n_checkpoint]

    def obtener_checkpoint_ant(self, n_checkpoint=0):
        """
        Dado el checkpoint actual, devuelve el anterior.
        :return: número de checkpoint anterior y sus coordenadas.
        """
        if n_checkpoint-1 >= 0:
            return n_checkpoint-1, self.checkpoints[n_checkpoint-1]
        else:
            return 0, self.checkpoints[0]

    def render(self, ventana):
        """
        Renderiza el entorno completo: paredes y checkpoints.
        """
        ventana.fill(self.COLOR)

        for i in range(len(self.recorrido) - 1):
            # Checkpoints
            if i < len(self.recorrido)-2:
                pygame.draw.line(ventana, (80, 80, 80), self.checkpoints[i, :2], self.checkpoints[i, 2:])
            # pygame.draw.line(ventana, (80, 80, 80), self.bordes1[i], self.bordes2[i], 3)

            # Carril central del recorrido
            # pygame.draw.aaline(ventana, (122, 122, 122), self.recorrido[i], self.recorrido[i+1])
            pygame.draw.line(ventana, (122, 122, 122), self.recorrido[i], self.recorrido[i + 1], 3)
            pygame.draw.circle(ventana, (200, 200, 200), self.recorrido[i + 1], 5, 0)

            # Bordes del recorrido
            pygame.draw.line(ventana, (255, 0, 0), self.bordes1[i], self.bordes1[i + 1], 3)
            pygame.draw.circle(ventana, (122, 0, 0), self.bordes1[i + 1], 5, 0)

            pygame.draw.line(ventana, (0, 0, 255), self.bordes2[i], self.bordes2[i + 1], 3)
            pygame.draw.circle(ventana, (0, 0, 122), self.bordes2[i + 1], 5, 0)
        #pygame.draw.line(ventana, (80, 80, 80), self.checkpoints[51, :2], self.checkpoints[51, 2:])


class Cohete:
    # VEL_MAX = 5
    VEL_ROT = 0.1
    ACELERACION = 0.5  # Aceleración lineal
    RAYOS = 7  # Número de rayos para realizar el raycast
    COLOR = (255, 255, 255)
    RADIO = 10

    def __init__(self, entorno, pos_inicial=(0, 0)):
        """
        Define el entorno y llama a inicializar.
        """
        self.entorno = entorno

        # Posición y orientación
        self.pos_inicial = pos_inicial  # Usado cuando se mueve el entorno en vez del cohete
        self.x = pos_inicial[0]
        self.y = pos_inicial[1]
        self.ang = 0  # Ángulo en radianes
        self.vector_movimiento = None

        # Velocidad
        self.dx = 0
        self.dy = 0

        # Checkpoints
        self.n_checkpoint, self.checkpoint = entorno.obtener_checkpoint_ant()
        self.n_checkpoint_sig, self.checkpoint_sig = entorno.obtener_checkpoint_sig()

        # Recompensa
        self.recompensa = 0

        # Raycast
        self.raycast = None

        # self.inicializar()

        print(self.checkpoint)
        print(self.checkpoint_sig)

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

        self.comprobar_colision_checkpoints()

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

        # El cohete avanza en función de su velocidad
        # self.x += self.dx
        # self.y += self.dy

        # Si queremos al cohete fijo en pantalla, entonces movemos el entorno
        self.entorno.mover(self.dx, self.dy)

        # Se calcula el vector movimiento para comprobar colisiones posteriormente
        # Contiene las componentes de posición en el instante inicial y en el posterior
        self.vector_movimiento = [self.x, self.y, self.x + self.dx, self.y + self.dy]

    def comprobar_colision_checkpoints(self):
        """
        Detecta si se ha traspasado un checkpoint o si se ha retrocedido (mediante vector movimiento),
        actualizando su cp actual, el anterior y el siguiente.
        """
        if self.interseccion(*self.vector_movimiento, *self.checkpoint_sig):
            # Si el cohete ha atravesado el siguiente checkpoint, avanzamos y actualizamos contadores y cps
            self.n_checkpoint, self.checkpoint = self.entorno.obtener_checkpoint_sig(self.n_checkpoint)
            self.n_checkpoint_sig, self.checkpoint_sig = self.entorno.obtener_checkpoint_sig(self.n_checkpoint)
            print(f"Último checkpoint:    {self.n_checkpoint}")
            print(f"Siguiente checkpoint: {self.n_checkpoint_sig}")
        elif self.interseccion(*self.vector_movimiento, *self.checkpoint):
            # Si el cohete ha atravesado el checkpoint anterior, retrocedemos el contador
            self.n_checkpoint, self.checkpoint = self.entorno.obtener_checkpoint_ant(self.n_checkpoint)
            self.n_checkpoint_sig, self.checkpoint_sig = self.entorno.obtener_checkpoint_sig(self.n_checkpoint)
            print()
            print(f"Último checkpoint:    {self.n_checkpoint}")
            print(f"Siguiente checkpoint: {self.n_checkpoint_sig}")
            print()

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

    def interseccion(self, x1, y1, x2, y2, x3, y3, x4, y4):
        denominador = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominador:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominador
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominador
            if 0 < t < 1 and 0 < u < 1:  # u>0 o 0 < u < 1
                return x1+t*(x2-x1), y1+t*(y2-y1)
        return None

    def render(self, ventana):
        """
        Renderiza el cohete
        """
        # pygame.draw.circle(ventana, self.COLOR, (self.x, self.y), 5.0)
        # pygame.draw.line(ventana, self.COLOR, (self.x, self.y), (self.x + np.cos(self.ang) * 10,
        #                                                         self.y + np.sin(self.ang) * 10))
        # Cuerpo del cohete
        pygame.gfxdraw.aacircle(ventana, int(self.x), int(self.y), self.RADIO, self.COLOR)
        pygame.gfxdraw.filled_circle(ventana, int(self.x), int(self.y), self.RADIO, self.COLOR)

        # Orientación
        pygame.draw.aaline(ventana, self.COLOR, (self.x, self.y), (self.x + np.cos(self.ang) * 2 * self.RADIO,
                                                                   self.y + np.sin(self.ang) * 2 * self.RADIO))

        # Vector velocidad
        pygame.draw.aaline(ventana, (0, 0, 122), self.vector_movimiento[:2], self.vector_movimiento[2:])

        # Marcar siguiente y anterior checkpoint
        pygame.draw.line(ventana, (0, 255, 255), self.checkpoint_sig[:2], self.checkpoint_sig[2:])
        pygame.draw.line(ventana, (255, 0, 255), self.checkpoint[:2], self.checkpoint[2:])


class Juego(gym.Env):
    def __init__(self, render=False):
        """
        Define action_space y observation_space. Contiene referencias a entorno y cohetes.
        Contiene ventana donde renderizar todo.
        """
        self.action_space = []
        self.observation_space = []

        # Atributos realizados con PyGame
        if not render:
            print("WARNING: Las opciones de renderizado no han sido activadas. Llamar a render() lanzará un error.\n"
                  "         Para activarlo, llame a inicializar_render().")
            self.clock = None
            self.ventana = None
            self.ancho = 0
            self.alto = 0
        else:
            self.inicializar_render()

        self.entorno = Entorno((self.ancho // 2, self.alto // 2))
        self.cohete = Cohete(self.entorno, (self.ancho // 2, self.alto // 2))

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

    def inicializar_render(self, ancho=800, alto=600):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.ventana = pygame.display.set_mode((ancho, alto))
        self.ancho = ancho
        self.alto = alto
