import gym


class Entorno:
    def __init__(self):
        """
        Llama a la función inicializar.
        """
        pass

    def inicializar(self):
        """
        Llama a la función generar_nivel, carga el número de checkpoints.
        """
        pass

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


class Cohete:
    def __init__(self):
        """
        Define el entorno y llama a inicializar.
        """
        pass

    def inicializar(self):
        """
        Define posición, velocidad, checkpoints, recompensa y actualiza raycast.
        """
        pass

    def actualizar(self):
        """
        Rota, acelera y mueve, comprueba colisiones, actualiza el raycast, actualiza las observaciones y su recompensa.
        """
        pass

    def rotar(self):
        """
        Rota el cohete y deja su angulo en [0, 2pi].
        """
        pass

    def acelerar(self):
        """
        Acelera el cohete (transforma su velocidad, no su posición).
        """
        pass

    def mover(self):
        """
        Rota, acelera y mueve el cohete, generando vector movimiento.
        """
        pass

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


class Juego(gym.Env):
    def __init__(self):
        """
        Define action_space y observation_space. Contiene referencias a entorno y cohetes.
        Contiene ventana donde renderizar todo.
        """
        pass

    def step(self, action):
        """
        Actualiza el cohete con su acción, comprueba estado colisión, obtiene las observaciones del cohete,
        obtiene las recompensas del cohete.
        :param action: acción que realiza el cohete.
        :return: o, r, d, i. (POR DEFINIR)
        """
        pass

    def reset(self):
        pass

    def render(self, mode="human"):
        """
        Renderiza el entorno, los cohetes y gui.
        :param mode: POR DEFINIR.
        :return: POR DEFINIR.
        """
        pass
