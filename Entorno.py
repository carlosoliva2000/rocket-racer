import gym
import pygame
import numpy as np

class Entorno(gym.Env):
    def __init__(self):
        pass

    def reset(self):
        return observation

    def step(self, action):
        pass

    def render(self, window, mode="human"):
        color=(100, 255, 0)
        window.fill(color)
        pygame.draw.line(window, (0, 0, 0), (random.randint(0, 1000), random.randint(0, 500)),
                         (random.randint(0, 1000), random.randint(0, 500)), 2)