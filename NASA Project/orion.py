import numpy
from ursina import *
from PIL import Image
from math import sin, cos, radians
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader, unlit_shader
import pandas as pd

app = Ursina()

space_texture = 'HDR_red_local_star.hdr'

space_sphere = Entity(
    model='sphere',
    texture=space_texture,
    scale=200,          
    double_sided=True,  
)

model = load_model('assets/orion-models/orion_capsule.obj')  

entity = Entity(model=model, scale=1, rotation_y=45)

def update():
    entity.rotation_y += 48 * time.dt

light = DirectionalLight(parent=entity)
light.look_at(entity)

player = FirstPersonController()
player.cursor.scale = 0.001  
player.speed = 25
player.gravity = 0
player.scale = 0.5

app.run()