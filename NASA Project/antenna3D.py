import numpy
from ursina import *
from PIL import Image
from math import sin, cos, radians
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader, unlit_shader
import pandas as pd
import time

app = Ursina()

space_texture = 'assets/textures-models/space-textures/HDR_red_local_star.hdr'

space_sphere = Entity(
    model='sphere',
    texture=space_texture,
    scale=1000,          
    double_sided=True
)

antenna = load_model('assets/textures-models/antenna-stuff/DSN_34.obj')

antenna_entity = Entity(model = antenna)



light = DirectionalLight(parent=antenna_entity)
light.look_at(antenna_entity)


player = FirstPersonController()
player.cursor.scale = 0.0001  
player.speed = 25
player.gravity = 0
player.scale = 0.5

def update():
    if held_keys['up arrow']:
        player.y += 10 * time.dt  # Move up
    if held_keys['down arrow']:
        player.y -= 10 * time.dt  # Move down
    if held_keys['escape']:
        exit(code=None)



app.run()