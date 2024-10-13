import timeit

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()


def input(key):
    if key == "escape" or key == "q":
        exit()
    earth.rotation_x += (held_keys['x'] * time.dt) * 1000
    earth.rotation_y += (held_keys['y'] * time.dt) * 1000
    camera.rotation_x += (held_keys['c'] * time.dt) * 100
    camera.rotation_y += (held_keys['v'] * time.dt) * 100
    camera.rotation_x -= (held_keys['b'] * time.dt) * 100
    camera.rotation_y -= (held_keys['n'] * time.dt) * 100
    move_speed = 10 * time.dt
    if held_keys['g']: camera.position += (move_speed, 0, 0)
    if held_keys['i']: camera.position -= (move_speed, 0, 0)
    if held_keys['h']: camera.position += (0, move_speed, 0)
    if held_keys['o']: camera.position -= (0, move_speed, 0)
    if held_keys['j']: camera.position += (0, 0, -move_speed)
    if held_keys['p']: camera.position -= (0, 0, -move_speed)


def update():
    earth.rotation_y -= 1
    moon.rotation_y -= 0.0366

class Planet:
    def __init__(self, scale, file, pos=(0, 0, 0)):
        self.entity = Entity(model="sphere", texture=file, scale=(scale, scale, scale), position=pos)
earth = Planet(2, "assets/textures-models/planet-textures/earth.jpg").entity
moon = Planet(0.54, "assets/textures-models/planet-textures/moon.jpg", pos=(60, 0, 0)).entity
earth.cull_faces, earth.double_sided = False, True
moon.cull_faces, moon.double_sided = False, True
EditorCamera()
Sky(texture="assets/textures-models/space-textures/space4.jpg")
mouse.locked = True
app.run()