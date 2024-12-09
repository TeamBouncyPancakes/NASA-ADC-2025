import numpy
from ursina import *
from PIL import Image
from math import sin, cos, radians
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader, unlit_shader
import pandas as pd
import time

app = Ursina()

z_offset = -5
slsbody = load_model('assets/textures-models/orion-models/orion_nasa_sls_body.glb')
slsbody_entity = Entity(model = slsbody, scale = (0.1,0.1,0.1), position=(10,2.98,z_offset))
slsbody_entity.rotation_z = 180
slsbody_entity.rotation_y = 90
slsnose = load_model('assets/textures-models/orion-models/orionmpcv.glb')
# slsnosetext = load_texture('assets/textures-models/orion-models/orion_mpcv.mtl')
slsnose_entity = Entity(model = slsnose, scale = (0.12,0.12,0.12), position = (4.1,-3.333,z_offset))
sls = Entity()
slsbody_entity.parent = sls
slsnose_entity.parent = sls

#txt = Text(text = "Artemis II mission.")

icps = load_model('assets/textures-models/orion-models/icpstextured.glb')
icps_entity = Entity(model=icps, scale=(0.014,0.014,0.014), position = (0.5,-2.8278,z_offset))
icps_entity.rotation_x = 90

capsule = load_model('assets/textures-models/orion-models/orioncapsuletextured.glb')
capsule_entity = Entity(model=capsule, scale = (1 , 1 , 1), position=(-13,-7.188,z_offset))
service_module = load_model('assets/textures-models/orion-models/servicemoduletextured.glb')
service_module_entity = Entity(model=service_module, scale = (1 , 1 , 1), position=(-4.6,-5.2,z_offset))
service_module_entity.origin =Vec3(1.4,0,0)
capsule_entity.rotation_y = 180

orion = Entity()

capsule_entity.parent = orion
service_module_entity.parent = orion
artemis2 = Entity()

sls.parent = artemis2
icps_entity.parent = artemis2
orion.parent = artemis2


capsule_entity.parent = artemis2
service_module_entity.parent = artemis2

artemis2.z = 20

light = DirectionalLight(parent=artemis2)
light.look_at(artemis2)

# Create a pivot for capsule and service module rotation
# capsule_pivot = Entity(parent=orion, position=capsule_entity.position)
# service_module_pivot = Entity(parent=orion, position=service_module_entity.position)

# capsule_entity.parent = capsule_pivot
# service_module_entity.parent = service_module_pivot


def update():
    # capsule_pivot.rotation_y += 1
    # service_module_pivot.rotation_y += 1
    
    # Rotate other parts (ICPS, nose, and body) independently if needed
    icps_entity.rotation_y += 1
    slsnose_entity.rotation_y += 1
    slsbody_entity.rotation_y += 1
    capsule_entity.z=0
    capsule_entity.rotation_y += 1
    service_module_entity.rotation_y += 1



#     if held_keys['up arrow']:
#         separate(slsnose_entity,artemis2)
#         translate_orion(slsnose_entity, 0,0.03, 0)
#     if held_keys['down arrow']:
#         separate(slsnose_entity,artemis2)
#         translate_orion(slsnose_entity, 0,-0.03, 0)
#     if held_keys['1']:
#         separate(orion_master,artemis2)
#         translate_orion(orion_master, 0, 0.01, 0)
#     if held_keys['2']:
#         separate(orion_master,artemis2)
#         translate_orion(orion_master, 0, -0.01, 0)
#     if held_keys['3']:
#         separate(orion,artemis2)
#         translate_orion(orion, 0, 0.01, 0)
#     if held_keys['4']:
#         separate(orion,artemis2)
#         translate_orion(orion, 0, -0.01, 0)
#     if held_keys['5']:
#         separate(capsule_entity,artemis2)
#         translate_orion(capsule_entity, 0, 0.01, 0)
#     if held_keys['6']:
#         separate(capsule_entity,artemis2)
#         translate_orion(capsule_entity, 0, -0.01, 0)
# #     # if held_keys['right arrow']:  
# #     #     rotate_orion(orion,5,0,0)
# #     # if held_keys['left arrow']:  
# #     #     rotate_orion(orion,-5,0,0)     
# #     # if held_keys['r']:  
# #     #     rotate_orion(orion,0,5,0)
# #     # if held_keys['l']:  
# #     #     rotate_orion(orion,0,-5,0)
    if held_keys['i']:
        player.y += 10 * time.dt  # Move up
    if held_keys['k']:
        player.y -= 10 * time.dt  # Move down
# #     if held_keys['escape']:
# #         exit(code=None


player = FirstPersonController()

player.cursor.scale = 0.0001


player.speed = 25
player.gravity = 0
player.scale = 0.5



app.run()

