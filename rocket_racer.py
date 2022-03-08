import sys
import gym
import numpy as np
import pygame
from pygame import gfxdraw


def interseccion(x1, y1, x2, y2, x3, y3, x4, y4):
    denominador = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominador:
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominador
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominador
        if 0 < t < 1 and 0 < u < 1:  # u>0 o 0 < u < 1
            return (x1 + t * (x2 - x1), y1 + t * (y2 - y1)), t
    return None


def proyeccion(x, y, x1, y1, x2, y2):
    if x1 == x2:
        return x1, y

    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    x_proyectado = (x * (1 / a) + y - b) * 1 / (a + 1 / a)
    y_proyectado = a * x_proyectado + b

    return x_proyectado, y_proyectado


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
        # Ejemplo de colisión descomentando el código posterior #
        # Ejemplos de semillas con colisión: 2928370872, 4084418319
        # semilla = int(np.random.rand()*(2**32 - 1))
        # np.random.seed(semilla)
        # print(semilla)
        self.generar_nivel()

    def generar_nivel(self):
        """
        Genera el nivel aleatorio, primero generando segmentos y luego aplicándoles anchura, y checkpoints.
        """
        longitud_min = 60
        longitud_max = 150
        d_ang = 0.5  # 0.8
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

        i = 1
        while i < segmentos:
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
            intersecta = False
            for j in range(i):
                x3 = recorrido[j, 0]
                y3 = recorrido[j, 1]
                x4 = recorrido[j+1, 0]
                y4 = recorrido[j+1, 1]
                intersecta = interseccion(x_ant, y_ant, x, y, x3, y3, x4, y4)
                if intersecta:
                    i = max(1, i-10)
                    break

            if not intersecta:
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

            # Aumentamos el contador
            i += 1

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
        if n_checkpoint + 1 < len(self.checkpoints):
            return n_checkpoint + 1, self.checkpoints[n_checkpoint + 1]
        else:
            return n_checkpoint, self.checkpoints[n_checkpoint]

    def obtener_checkpoint_ant(self, n_checkpoint=0):
        """
        Dado el checkpoint actual, devuelve el anterior.
        :return: número de checkpoint anterior y sus coordenadas.
        """
        if n_checkpoint - 1 >= 0:
            return n_checkpoint - 1, self.checkpoints[n_checkpoint - 1]
        else:
            return 0, self.checkpoints[0]

    def render(self, ventana):
        """
        Renderiza el entorno completo: paredes y checkpoints.
        """
        ventana.fill(self.COLOR)

        for i in range(len(self.recorrido) - 1):
            # Checkpoints
            if i < len(self.recorrido) - 2:
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
        # pygame.draw.line(ventana, (80, 80, 80), self.checkpoints[51, :2], self.checkpoints[51, 2:])


class Cohete:
    VEL_MAX_CUADRADADA = 900
    VEL_ROT = 0.1
    ACELERACION = 0.5  # Aceleración lineal
    RAYOS = 7  # Número de rayos para realizar el raycast
    COLOR_ACTIVO = (255, 255, 255)
    COLOR_INACTIVO = (0, 0, 0)
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
        self.xp = None
        self.yp = None
        self.xp_sig = None
        self.yp_sig = None

        # Observaciones
        self.observaciones = None

        # Recompensa
        self.recompensa = 0

        # Flags
        self.flag_colision = False

        # Raycast
        # self.rayos = [Rayo(self, 0, 100)]
        self.rayos = [Rayo(self, np.pi / 2), Rayo(self, np.pi / 4), Rayo(self, 0),
                      Rayo(self, -np.pi / 4), Rayo(self, -np.pi / 2)]

        # Color
        self.color = self.COLOR_ACTIVO

    def inicializar(self, pos_inicial=(0, 0)):
        """
        Define posición, velocidad, checkpoints, recompensa y actualiza raycast.
        """
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
        self.n_checkpoint, self.checkpoint = self.entorno.obtener_checkpoint_ant()
        self.n_checkpoint_sig, self.checkpoint_sig = self.entorno.obtener_checkpoint_sig()
        self.xp = None
        self.yp = None
        self.xp_sig = None
        self.yp_sig = None

        # Observaciones
        self.observaciones = None

        # Recompensa
        self.recompensa = 0

        # Flags
        self.flag_colision = False

        # Raycast
        # self.rayos = [Rayo(self, 0, 100)]
        self.rayos = [Rayo(self, np.pi / 2), Rayo(self, np.pi / 4), Rayo(self, 0),
                      Rayo(self, -np.pi / 4), Rayo(self, -np.pi / 2)]

        # Actualiza el raycast y las observaciones
        self.actualizar_raycast()
        self.actualizar_observaciones()

        # Color
        self.color = self.COLOR_ACTIVO

    def actualizar(self, accion):
        """
        Rota, acelera y mueve, comprueba colisiones, actualiza el raycast, actualiza las observaciones y su recompensa.
        """
        self.mover(accion)

        self.comprobar_colision_checkpoints()
        self.comprobar_colision_entorno()

        self.actualizar_raycast()

        self.actualizar_observaciones()
        self.actualizar_recompensa()

    def rotar(self, rotacion):
        """
        Rota el cohete y deja su angulo en [-pi, pi].
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
        self.vector_movimiento = [self.x, self.y, self.x - self.dx, self.y - self.dy]

    def comprobar_colision_checkpoints(self):
        """
        Detecta si se ha traspasado un checkpoint o si se ha retrocedido (mediante vector movimiento),
        actualizando su cp actual, el anterior y el siguiente.
        """
        # Comprobamos colisiones hacia adelante partiendo desde la posición del cohete
        # Este código es el equivalente al primer if, pero no funciona porque es necesario comprobar
        # necesariamente todos los checkpoints, ya que la detección de colisión con el siguiente no es exacta
        colision = False
        for i in range(self.n_checkpoint_sig, len(self.entorno.checkpoints)):
            checkpoint = self.entorno.checkpoints[i]
            if interseccion(*self.vector_movimiento, *checkpoint):
                # if i != self.n_checkpoint_sig:
                #     print(f"HE SALTADO {i-self.n_checkpoint} PASOS")

                self.n_checkpoint, self.checkpoint = i, checkpoint
                self.n_checkpoint_sig, self.checkpoint_sig = self.entorno.obtener_checkpoint_sig(self.n_checkpoint)
                colision = True
                break

        # Si no hay colisión hacia adelante, puede haber ido hacia atrás
        # Por la misma razón que antes, este es el equivalente al elif de abajo
        if not colision:
            for i in range(self.n_checkpoint_sig, -1, -1):
                checkpoint = self.entorno.checkpoints[i]
                if interseccion(*self.vector_movimiento, *checkpoint):
                    # if i != self.n_checkpoint:
                    #    print(f"HE SALTADO {self.n_checkpoint_sig-i} PASOS")
                    self.n_checkpoint, self.checkpoint = self.entorno.obtener_checkpoint_ant(i)
                    self.n_checkpoint_sig, self.checkpoint_sig = self.entorno.obtener_checkpoint_sig(self.n_checkpoint)
                    break

        """
        #### CÓDIGO DEPRECADO/OBSOLETO ####
        if self.interseccion(*self.vector_movimiento, *self.checkpoint_sig):
            # Si el cohete ha atravesado el siguiente checkpoint, avanzamos y actualizamos contadores y cps
            self.n_checkpoint, self.checkpoint = self.entorno.obtener_checkpoint_sig(self.n_checkpoint)
            self.n_checkpoint_sig, self.checkpoint_sig = self.entorno.obtener_checkpoint_sig(self.n_checkpoint)
            #print(f"Último checkpoint:    {self.n_checkpoint}")
            print(f"Siguiente checkpoint: {self.n_checkpoint_sig}")
        elif self.interseccion(*self.vector_movimiento, *self.checkpoint):
            # Si el cohete ha atravesado el checkpoint anterior, retrocedemos el contador
            self.n_checkpoint, self.checkpoint = self.entorno.obtener_checkpoint_ant(self.n_checkpoint)
            self.n_checkpoint_sig, self.checkpoint_sig = self.entorno.obtener_checkpoint_sig(self.n_checkpoint)
            #print(f"Último checkpoint:    {self.n_checkpoint}")
            print(f"Siguiente checkpoint: {self.n_checkpoint_sig}")
        """

    def comprobar_colision_entorno(self):
        """
        Detecta si se ha colisionado con un elemento del entorno (mediante vector movimiento). Activa flag_colision.
        """
        for i in range(len(self.entorno.recorrido) - 1):
            # Comprobamos si se ha atravesado una pared mediante vector movimiento
            if (interseccion(*self.vector_movimiento, *self.entorno.bordes1[i], *self.entorno.bordes1[i + 1]) or
                    interseccion(*self.vector_movimiento, *self.entorno.bordes2[i], *self.entorno.bordes2[i + 1])):
                self.color = self.COLOR_INACTIVO
                # print("HE ATRAVESADO")
                self.flag_colision = True
                break

    def actualizar_raycast(self):
        """
        Actualiza cada rayo, colocándolo alrededor del cohete y definiendo su longitud.
        """
        for rayo in self.rayos:
            rayo.actualizar()

    def actualizar_observaciones(self):
        """
        Almacena en observaciones las distancias de los rayos y otras necesarias.
        """
        # Distancias de todos los rayos
        dist_rayos_interp = [r.longitud_interp for r in self.rayos]

        # Velocidad del cohete
        velocidad = self.dx ** 2 + self.dy ** 2
        velocidad_interp = np.interp(velocidad, [0, self.VEL_MAX_CUADRADADA], [-1, 1])

        # Diferencia angular entre orientación y vector velocidad
        angulo_vel = np.arctan2(self.dy, self.dx)
        if velocidad == 0.0:
            dif_ang = 0.0
        else:
            dif_ang = np.clip(angulo_vel - self.ang, -np.pi, np.pi)
        dif_ang_interp = np.interp(dif_ang, [-np.pi, np.pi], [-1, 1])

        # Diferencia angular entre orientación y punto más cercano del siguiente checkpoint
        # Primero, calculamos la proyección perpendicular en el siguiente checkpoint
        self.xp, self.yp = proyeccion(self.x, self.y, *self.checkpoint)
        self.xp_sig, self.yp_sig = proyeccion(self.x, self.y, *self.checkpoint_sig)

        # Segundo, calculamos la distancia entre la posición y el punto proyectado
        dx = self.xp_sig - self.x
        dy = self.yp_sig - self.y

        # Tercero, como anteriormente, calculamos la diferencia angular
        ang_proyeccion = np.arctan2(dy, dx)
        dif_ang_proyeccion = np.clip(ang_proyeccion - self.ang, -np.pi, np.pi)
        dif_ang_proyeccion_interp = np.interp(dif_ang_proyeccion, [-np.pi, np.pi], [-1, 1])

        self.observaciones = np.concatenate((dist_rayos_interp,
                                             (velocidad_interp, dif_ang_interp, dif_ang_proyeccion_interp)))

    def actualizar_recompensa(self):
        """
        Almacena en recompensa los puntos obtenidos en esa actualización.
        """
        #self.recompensa = float(self.n_checkpoint)
        dist_cp = np.sqrt((self.x-self.xp)**2+(self.y-self.yp)**2)
        dist_cp_sig = np.sqrt((self.x-self.xp_sig)**2+(self.y-self.yp_sig)**2)
        self.recompensa = self.n_checkpoint + 1 * (dist_cp/(dist_cp+dist_cp_sig))
        #self.reward_total = self.n_lap * self.env.n_goals + self.level + 1 * (distance0/(distance0+distance1))
        #self.reward_step = self.reward_total - reward_total_previous

    def render(self, ventana):
        """
        Renderiza el cohete
        """
        # Renderizar rayos
        for rayo in self.rayos:
            rayo.render(ventana)

        # pygame.draw.circle(ventana, self.COLOR, (self.x, self.y), 5.0)
        # pygame.draw.line(ventana, self.COLOR, (self.x, self.y), (self.x + np.cos(self.ang) * 10,
        #                                                         self.y + np.sin(self.ang) * 10))
        # Cuerpo del cohete
        pygame.gfxdraw.aacircle(ventana, int(self.x), int(self.y), self.RADIO, self.color)
        pygame.gfxdraw.filled_circle(ventana, int(self.x), int(self.y), self.RADIO, self.color)

        # Orientación
        pygame.draw.aaline(ventana, self.color, (self.x, self.y), (self.x + np.cos(self.ang) * 2 * self.RADIO,
                                                                   self.y + np.sin(self.ang) * 2 * self.RADIO))

        # Vector velocidad
        pygame.draw.aaline(ventana, (0, 0, 122), self.vector_movimiento[:2], self.vector_movimiento[2:])

        # Marcar siguiente y anterior checkpoint
        pygame.draw.line(ventana, (0, 255, 255), self.checkpoint_sig[:2], self.checkpoint_sig[2:])
        pygame.draw.line(ventana, (255, 0, 255), self.checkpoint[:2], self.checkpoint[2:])
        pygame.draw.circle(ventana, (255, 255, 255), (self.xp, self.yp), 4)
        pygame.draw.circle(ventana, (255, 255, 255), (self.xp_sig, self.yp_sig), 4)


class Rayo:
    COLOR = (0, 255, 0)

    def __init__(self, cohete, ang_offset, longitud_maxima = 1000):
        self.cohete = cohete
        self.x1 = cohete.x
        self.y1 = cohete.y
        self.ang = ang_offset
        self.ang_offset = ang_offset
        self.x2 = cohete.x
        self.y2 = cohete.y
        self.longitud_maxima = longitud_maxima
        self.longitud = longitud_maxima
        self.longitud_interp = 1
        self.flag_interseccion = False

    def actualizar(self):
        # Actualizamos poisición en función de la del cohete
        self.x1 = self.cohete.x
        self.y1 = self.cohete.y

        # Actualizamos ángulo en función del ángulo del cohete
        self.ang = self.ang_offset + self.cohete.ang

        # Actualizamos puntos de destino
        self.x2 = self.x1 + np.cos(self.ang) * self.longitud_maxima
        self.y2 = self.y1 + np.sin(self.ang) * self.longitud_maxima

        # Comprobamos colisiones con entorno para ajustar el rayo
        pts_corte = None
        dist_min = 1
        for i in range(len(self.cohete.entorno.bordes1) - 1):
            # Primero comprobamos intersección para bordes 1
            res_borde = interseccion(self.x1, self.y1, self.x2, self.y2,
                                     *self.cohete.entorno.bordes1[i], *self.cohete.entorno.bordes1[i + 1])
            # Si se devuelve una intersección con los bordes 1, entonces comprobamos si es mínimo
            if res_borde:
                pts_borde, dist_borde = res_borde
                if dist_borde < dist_min:
                    dist_min = dist_borde
                    pts_corte = pts_borde

            res_borde = interseccion(self.x1, self.y1, self.x2, self.y2,
                                     *self.cohete.entorno.bordes2[i], *self.cohete.entorno.bordes2[i + 1])
            # Si se devuelve una intersección con los bordes 2, entonces comprobamos si es mínimo
            if res_borde:
                pts_borde, dist_borde = res_borde
                if dist_borde < dist_min:
                    dist_min = dist_borde
                    pts_corte = pts_borde

        # Si existe un punto de corte (ya calculado como el mínimo), entonces lo establecemos como (x2, y2)
        if pts_corte:
            self.x2, self.y2 = pts_corte
            self.longitud = dist_min * self.longitud_maxima
            self.longitud_interp = np.interp(self.longitud, [0, self.longitud_maxima], [-1, 1])
            self.flag_interseccion = True
        else:
            self.longitud = self.longitud_maxima
            self.longitud_interp = 1
            self.flag_interseccion = False

    def render(self, ventana):
        """
        Renderiza el rayo.
        :param ventana: display o ventana donde se mostrará el rayo
        """
        pygame.draw.aaline(ventana, self.COLOR, (self.x1, self.y1), (self.x2, self.y2))


class Juego(gym.Env):
    def __init__(self, env_config=None):
        """
        Define action_space y observation_space. Contiene referencias a entorno y cohetes.
        Contiene ventana donde renderizar todo.
        """
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(2,))
        self.observation_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(8,))

        # Obtenemos opciones de configuración del entorno
        if env_config:
            render = env_config['render']
        else:
            render = False

        # Atributos realizados con PyGame
        if not render:
            print("WARNING: Las opciones de renderizado no han sido activadas. Llamar a render() lanzará un error.\n"
                  "         Para activarlo, llame a inicializar_render().")
            self.clock = None
            self.ventana = None
            self.ancho = 0
            self.alto = 0
            self.fuente = None
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

        return self.cohete.observaciones, self.cohete.recompensa, self.cohete.flag_colision, {}

    def reset(self):
        # Reiniciar el entorno
        self.entorno.inicializar()

        # Reiniciar el cohete
        self.cohete.inicializar((self.ancho // 2, self.alto // 2))

        return self.cohete.observaciones

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

        # Renderizamos la GUI
        self.imprimir_texto(f"Recompensa: {self.cohete.recompensa}", 10, 10)
        self.imprimir_texto(f"Checkpoint: {self.cohete.n_checkpoint}", 10, 30)
        self.imprimir_texto(f"Colisión: {self.cohete.flag_colision}", 10, 50)
        self.imprimir_texto(f"Velocidad: {self.cohete.dx**2 + self.cohete.dy**2}", 10, 70)

        # Actualizamos la pantalla con el frame generado
        pygame.display.update()

    def inicializar_render(self, ancho=800, alto=600):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.ventana = pygame.display.set_mode((ancho, alto))
        self.ancho = ancho
        self.alto = alto
        self.fuente = pygame.font.Font(pygame.font.get_default_font(), 20)

    def imprimir_texto(self, texto, x, y):
        texto_surface = self.fuente.render(texto, True, (255, 255, 255))
        texto_rect = texto_surface.get_rect()
        texto_rect.topleft = (x, y)
        self.ventana.blit(texto_surface, texto_rect)
