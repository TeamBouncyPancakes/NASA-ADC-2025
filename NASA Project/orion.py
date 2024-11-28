import numpy
from ursina import *
from PIL import Image
from math import sin, cos, radians
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader, unlit_shader
import pandas as pd
<<<<<<< HEAD

app = Ursina()

space_texture = 'HDR_red_local_star.hdr'
=======
import time

app = Ursina()

space_texture = 'assets/textures-models/space-textures/HDR_red_local_star.hdr'
>>>>>>> 6f6b3e9af1fbf764bbe26f6fc0b16e5abc36d3f0

space_sphere = Entity(
    model='sphere',
    texture=space_texture,
<<<<<<< HEAD
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
=======
    scale=100,
    double_sided=True
)

space_sphere.layer = 0


service_module = load_model('assets/textures-models/orion-models/orion_service_module.obj')
capsule = load_model('assets/textures-models/orion-models/orion_capsule_new.obj')



capsule_entity = Entity(model=capsule,rotation_y=45, position=(0,0,0))
service_module_entity = Entity(model=service_module, scale = 1, rotation_y=45, position=(0,1.2,0))

orion = Entity()

capsule_entity.parent = orion
service_module_entity.parent = orion

light = DirectionalLight(parent=service_module_entity)
light.look_at(service_module_entity)

light = DirectionalLight(parent=capsule_entity)
light.look_at(capsule_entity)


player = FirstPersonController()

player.cursor.scale = 0.0001


>>>>>>> 6f6b3e9af1fbf764bbe26f6fc0b16e5abc36d3f0
player.speed = 25
player.gravity = 0
player.scale = 0.5

<<<<<<< HEAD
app.run()
=======


app.run()

>>>>>>> 6f6b3e9af1fbf764bbe26f6fc0b16e5abc36d3f0
