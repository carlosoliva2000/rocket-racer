import pygame

from rocket_racer import *


def manejar_eventos(eventos):
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return 1
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            return 2
    return 0


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


juego = Juego(env_config={'render': True})
# juego.inicializar_render()

while True:
    evento = manejar_eventos(pygame.event.get())
    if evento == 1:
        break
    elif evento == 2:
        juego.reset()

    accion = manejar_entrada(list(pygame.key.get_pressed()))

    # Acción random
    # accion = [np.random.randint(-1, 2) * np.random.rand(), np.random.randint(-1, 2) * np.random.rand()]

    juego.step(accion)
    juego.render()
    juego.clock.tick(30)
