import numpy
from ursina import *
from PIL import Image
from math import sin, cos, radians
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader, unlit_shader
import pandas as pd
import time

app = Ursina()
main_camera = camera
secondary_camera = Entity(name='secondary_camera', camera=True)
secondary_camera.position = (5, 5, -10)  # Position it differently
secondary_camera.look_at(Vec3(0, 0, 0))  # Look at the origin

secondary_camera.enabled=True
camera.enabled=False

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

capsule_entity = Entity(model=capsule, position=(0,0,0))
service_module_entity = Entity(model=service_module, scale = 1, position=(0,1.2,0))

orion = Entity(scale = (0.2,0.2,0.2))
orion.position=(0, 0, 0.75)

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


def separate(e1,e2):
        e1.parent = None
        e2.parent = None

sample_trajectory_points = [Vec3(-3, 0, 0), Vec3(0, 0, 3), Vec3(3, 0, 0), Vec3(0, 0, -3)]

c = 0
# def rotate_vector(vector, angle):
#     """Rotate a vector around the Y-axis by a given angle in degrees."""
#     radians = math.radians(angle)
#     new_x = vector.x * cos(radians) - vector.z * sin(radians)
#     new_z = vector.x * sin(radians) + vector.z * cos(radians)
#     return Vec3(new_x, vector.y, new_z)

def update():
    if held_keys['escape']:
        exit()

    
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
    global c
    if c<4:
        i=sample_trajectory_points[c]
        direction = (i - orion.position).normalized()
        orion.position += direction * 1 * time.dt
    
    if direction.length() > 0:
            # Calculate the angle in radians
        target_rotation_y = math.degrees(math.atan2(direction.x, direction.y))
        orion.rotation_y = lerp(orion.rotation_y, target_rotation_y, 5 * time.dt)

            # Update the front's orientation to match the direction of movement
        tp = orion.position + direction
        orion.look_at(tp)
        if orion.rotation_y>0:
            orion.rotation_y+=90
        else:
            orion.rotation_y-=90
        
    light = DirectionalLight(parent=orion)
    light.look_at(orion)

    

    if (orion.position - i).length() < 0.1:
        c = (c+1)%4

        

# light = DirectionalLight(parent=service_module_entity)
# light.look_at(service_module_entity)

# light = DirectionalLight(parent=capsule_entity)
# light.look_at(capsule_entity)

light = DirectionalLight(parent=orion)
light.look_at(orion)


player = FirstPersonController()
player.position=(0, 0, 0.75)
player.cursor.scale = 0.0001  
player.speed = 25
player.gravity = 0
player.scale = 0.5

camera.position = (0, 5, -10)
camera.rotation_x = 30
# secondary_camera.enabled=True
# camera.enabled=False

app.run()
