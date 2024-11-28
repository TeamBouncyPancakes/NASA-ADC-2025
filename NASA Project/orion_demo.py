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
    scale=100,          
    double_sided=True  
)

space_sphere.layer = 0 

service_module = load_model('assets/textures-models/orion-models/orion_service_module.obj')
capsule = load_model('assets/textures-models/orion-models/orion_capsule_new.obj')

capsule_entity = Entity(model=capsule,rotation_y=45, position=(0,0,0))
service_module_entity = Entity(model=service_module, scale = 1, rotation_y=45, position=(0,1.2,0))

orion = Entity()
# orion.layer=1

# light = DirectionalLight(parent=orion)
# light.look_at(orion)

capsule_entity.parent = orion
service_module_entity.parent = orion

def rotate_orion(e , x , y , z):
    e.rotation_y += x
    e.rotation_x += y
    e.rotation_z += z

def translate_orion(e , x , y , z):
     e.x += x
     e.y += y
     e.z += z

#rotate_orion(orion,0,0,1.5)

def separate(e1,e2):
        e1.parent = None
        e2.parent = None


def update():
    if held_keys['escape']:
        exit()

    #rotate_orion(orion,0.1,0,0)
    
    if held_keys['up arrow']: 
        separate(capsule_entity,service_module_entity)
        translate_orion(capsule_entity, 0,0.01,0)
    if held_keys['down arrow']:  
        separate(capsule_entity,service_module_entity)
        translate_orion(capsule_entity, 0,-0.01,0)
    if held_keys['right arrow']:  
        rotate_orion(orion,5,0,0)
    if held_keys['left arrow']:  
        rotate_orion(orion,-5,0,0)     
    if held_keys['r']:  
        rotate_orion(orion,0,5,0)
    if held_keys['l']:  
        rotate_orion(orion,0,-5,0)



light = DirectionalLight(parent=service_module_entity)
light.look_at(service_module_entity)

light = DirectionalLight(parent=capsule_entity)
light.look_at(capsule_entity)


player = FirstPersonController()
player.cursor.scale = 0.0001  
player.speed = 25
player.gravity = 0
player.scale = 0.5


app.run()