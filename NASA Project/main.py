import timeit

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()


def input(key):
    if key == "escape" or key == "q":
        exit()
    earth.x -= held_keys['a'] * time.dt * 10
    earth.x += held_keys['d'] * time.dt * 10
    earth.y += held_keys['w'] * time.dt * 10
    earth.y -= held_keys['s'] * time.dt * 10
    scale_increment = 0.5
    if held_keys['k']:
        earth.scale += (scale_increment, scale_increment, scale_increment)
    if held_keys['m']:
        earth.scale -= (scale_increment, scale_increment, scale_increment)
    earth.rotation_x += (held_keys['x'] * time.dt) * 1000
    earth.rotation_y += (held_keys['y'] * time.dt) * 1000
    camera.rotation_x += (held_keys['c'] * time.dt) * 100
    camera.rotation_y += (held_keys['v'] * time.dt) * 100
    camera.rotation_x -= (held_keys['b'] * time.dt) * 100
    camera.rotation_y -= (held_keys['n'] * time.dt) * 100
    camera.position = (
        camera.position[0] + (held_keys['g'] * time.dt * 10) - (held_keys['i'] * time.dt * 10),
        camera.position[1] + (held_keys['h'] * time.dt * 10) - (held_keys['o'] * time.dt * 10),
        camera.position[2] + (held_keys['j'] * time.dt * 10) - (held_keys['p'] * time.dt * 10)
    )


#not working for some reason
def update():
    pass
class Planet:
    def __init__(self, tripscale):
        self.entity = Entity(model="sphere", texture="assets/textures-models/planet-textures/earth.jpg", scale=(tripscale, tripscale, tripscale))
earth = Planet(2).entity
earth.cull_faces, earth.double_sided = False, True
EditorCamera()
mouse.locked = True
app.run()