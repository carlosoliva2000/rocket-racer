from rocket_racer import *


def manejar_eventos(eventos):
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return True
    return False


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


juego = Juego(render=True)
# juego.inicializar_render()

while True:
    if manejar_eventos(pygame.event.get()):
        break

    accion = manejar_entrada(list(pygame.key.get_pressed()))
    juego.step(accion)
    juego.render()
    juego.clock.tick(30)
