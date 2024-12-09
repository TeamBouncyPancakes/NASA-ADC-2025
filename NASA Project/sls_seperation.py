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

# space_sphere = Entity(
#     model='sphere',
#     texture=space_texture,
#     scale=300,
#     double_sided=True
# )

# space_sphere.layer = 0

slsbody = load_model('assets/textures-models/orion-models/orion_nasa_sls_body.glb')

slsbody_entity = Entity(model = slsbody, scale = (0.12,0.12,0.12))
slsbody_entity.rotation_z = 180
slsbody_entity.y = 0.45
slsnose = load_model('assets/textures-models/orion-models/orionmpcv.glb')
slsnose_entity = Entity(model = slsnose, scale = (0.12,0.12,0.12))
slsnose_entity.y = 10
icps = load_model('assets/textures-models/orion-models/icpstextured.glb')
service_module = load_model('assets/textures-models/orion-models/servicemoduletextured.glb')
capsule = load_model('assets/textures-models/orion-models/orioncapsuletextured.glb')
capsule_entity = Entity(model=capsule, position=(-1.8,3.21,-0.4))
service_module_entity = Entity(model=service_module, scale = 1, position=(-3.5,1.2,0))
orion = Entity(scale = (0.2,0.2,0.2))
orion.position=(0, 0, 0)
capsule_entity.parent = orion
service_module_entity.parent = orion
icps_entity = Entity(model=icps, scale=0.008, position = (-0.33,0.3,0))
icps_entity.rotation_x = -90
icps_entity.rotation_x = 90
orion_master = Entity(scale = (1,1,1))
icps_entity.parent = orion_master
orion.parent = orion_master
# sls.parent = orion_master   
orion_master.y = 9.8
orion_master.x = 0.33
artemis2 = Entity(scale = (3,3,3))
slsbody_entity.parent = artemis2
slsnose_entity.parent = artemis2
orion_master.parent = artemis2
# orion_master.z = -0.5
slsbody_entity.rotation_y = 90
# light = DirectionalLight(parent=artemis2)
# light.look_at(artemis2)
ambient_light = AmbientLight()
ambient_light.intensity = 0.3

# def rotate_orion(e , x , y , z):
#     e.rotation_y += x
#     e.rotation_x += y
#     e.rotation_z += zs

# def translate_orion(e , x , y , z):
#      e.x += x
#      e.y += y
#      e.z += z


# def separate(e1,e2):
#         e1.parent = None
#         e2.parent = None

def update():
    if held_keys['up arrow']:
        print('hello')
        # separate(slsnose_entity,artemis2)
    #     # translate_orion(slsnose_entity, 0,0.03, 0)
        slsnose_entity.y += 0.03
    if held_keys['down arrow']:
        slsnose_entity.y += 0.03
    if held_keys['1']:
        orion_master.y += 0.01
    if held_keys['2']:
        orion_master.y -= 0.01
    if held_keys['3']:
        orion.y += 0.01
    if held_keys['4']:
        orion.y -= 0.01
    if held_keys['5']:
        capsule_entity.y += 0.01
    if held_keys['6']:
        capsule_entity.y -= 0.01
    artemis2.rotation_y = 180


    
    # if held_keys['0']:
    #     separate(slsnose_entity,artemis2)
    #     translate_orion(slsnose_entity, 0,0.1, 0)
    #     separate(orion_master,artemis2)
    #     translate_orion(orion_master, 0, 0.08, 0)
    #     separate(orion,artemis2)
    #     time.sleep(5)
    #     translate_orion(orion, 0, 0.03, 0)
    #     separate(capsule_entity,artemis2)
    #     translate_orion(capsule_entity, 0, 0.01, 0)

#     # if held_keys['right arrow']:  
#     #     rotate_orion(orion,5,0,0)
#     # if held_keys['left arrow']:  
#     #     rotate_orion(orion,-5,0,0)     
#     # if held_keys['r']:  
#     #     rotate_orion(orion,0,5,0)
#     # if held_keys['l']:  
#     #     rotate_orion(orion,0,-5,0)
    if held_keys['i']:
        player.y += 10 * time.dt  # Move up
    if held_keys['k']:
        player.y -= 10 * time.dt  # Move down
#     if held_keys['escape']:
#         exit(code=Noneseparate(orion_master,artemis2)
        # translate_


player = FirstPersonController()

player.cursor.scale = 0.0001


player.speed = 25
player.gravity = 0
player.scale = 0.5



app.run()

