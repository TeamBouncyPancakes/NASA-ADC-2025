import numpy
from ursina import *
from PIL import Image
from math import sin, cos, radians
from ursina.shaders import lit_with_shadows_shader, unlit_shader
import pandas as pd
import time

app = Ursina()

z_offset = -5
slsbody = load_model('assets/textures-models/orion-models/orion_nasa_sls_body.glb')
slsbody_entity = Entity(model=slsbody, scale=(0.1, 0.1, 0.1), position=(10, 2.98, z_offset))
slsbody_entity.rotation_z = 180
slsbody_entity.rotation_y = 90
slsnose = load_model('assets/textures-models/orion-models/orionmpcv.glb')
slsnose_entity = Entity(model=slsnose, scale=(0.12, 0.12, 0.12), position=(4.1, -3.333, z_offset))
sls = Entity()
slsbody_entity.parent = sls
slsnose_entity.parent = sls


icps = load_model('assets/textures-models/orion-models/icpstextured.glb')
icps_entity = Entity(model=icps, scale=(0.014, 0.014, 0.014), position=(0.5, -2.8278, z_offset))
icps_entity.rotation_x = 90

capsule = load_model('assets/textures-models/orion-models/orioncapsuletextured.glb')
capsule_entity = Entity(model=capsule, scale=(1, 1, 1), position=(-13, -7.188, z_offset))
service_module = load_model('assets/textures-models/orion-models/servicemoduletextured.glb')
service_module_entity = Entity(model=service_module, scale=(1, 1, 1), position=(-4.6, -5.2, z_offset))
service_module_entity.origin = Vec3(1.4, 0, 0)
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

Sky(texture="assets/textures-models/space-textures/space4.jpg")
panel = Entity(
    parent=camera.ui,
    model='quad',
    color=color.white,
    scale=(0.777, 2),
    position=(-0.7, 0.5, 1)
)

title = Text('Model Viewer', parent=camera.ui)
title.color = color.black
title.scale = (2, 2)
(title.x, title.y, title.z) = (-0.7, 0.45, -1)

model_entities = [capsule_entity, service_module_entity, icps_entity, slsnose_entity, slsbody_entity]
model_buttons = []

for model in model_entities:
    model.position = (0, 0, 0)

def choose(name):
    for entity in model_entities:
        entity.visible = False
    if name == "Orion":
        capsule_entity.visible = True
    elif name == "Service Module":
        service_module_entity.visible = True
    elif name == "ICPS":
        icps_entity.visible = True
    elif name == "SLS: Nose":
        slsnose_entity.visible = True
    else:
        slsbody_entity.visible = True
    print(name)

counter = 0.3
for name in ["Orion", "Service Module", "ICPS", "SLS: Nose", "SLS: Body"]:
    button = Button(text=name, position=(-0.56, counter, -1), scale=(0.25, 0.125))
    model_buttons.append(button)
    counter -= 0.175
    print(counter)
counter2 = 0
for button_thing in model_buttons:
    if counter2 == 0:
        button_thing.on_click = lambda:choose("Orion")
    elif counter2 == 1:
        button_thing.on_click = lambda:choose("Service Module")
    elif counter2 == 2:
        button_thing.on_click = lambda: choose("ICPS")
    elif counter2 == 3:
        button_thing.on_click = lambda: choose("SLS: Nose")
    else:
        button_thing.on_click = lambda: choose("SLS: Body")
    counter2 += 1


artemis2.z = 20

light = DirectionalLight(parent=artemis2)
light.look_at(artemis2)


def input(inp):
    if held_keys['esc']:
        exit()

def update():
 
    icps_entity.rotation_y += 1
    slsnose_entity.rotation_y += 1
    slsbody_entity.rotation_y += 1
    capsule_entity.z = 0
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
    #         if held_keys['right arrow']:
    #             rotate_orion(orion,5,0,0)
    #         if held_keys['left arrow']:
    #             rotate_orion(orion,-5,0,0)
    #         if held_keys['r']:
    #             rotate_orion(orion,0,5,0)
    #         if held_keys['l']:
    #             rotate_orion(orion,0,-5,0)
    if held_keys['i']:
        player.y += 10 * time.dt  # Move up
    if held_keys['k']:
        player.y -= 10 * time.dt  # Move down




player = EditorCamera()


player.speed = 25
player.gravity = 0
player.scale = 0.5

app.run()

