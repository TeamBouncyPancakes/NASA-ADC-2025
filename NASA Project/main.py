import timeit

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()


def input(key):
    if key == "escape" or key == "q":
        exit()
    earth.x += held_keys['a'] * time.dt
    earth.x -= held_keys['d'] * time.dt
    earth.y += held_keys['w'] * time.dt
    earth.y -= held_keys['s'] * time.dt
    scale_increment = 0.5
    if held_keys['b']:
        earth.scale += (scale_increment, scale_increment, scale_increment)
    if held_keys['m']:
        earth.scale -= (scale_increment, scale_increment, scale_increment)
    earth.rotation_x += (held_keys['x'] * time.dt) * 1000
    earth.rotation_y += (held_keys['y'] * time.dt) * 1000
#not working for some reason
def update():
    pass
class Planet:
    def __init__(self):
        self.entity = Entity(model="sphere", texture="assets/textures-models/planet-textures/earth.jpg")
earth = Planet().entity
app.run()