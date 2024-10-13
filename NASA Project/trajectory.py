import pandas as pd
from ursina import *
import numpy as np


ms_data = pd.read_csv('middle-school-data.csv')

x_velocity = ms_data['Vx(km/s)[J2000-EARTH]'].to_numpy()
y_velocity = ms_data['Vy(km/s)[J2000-EARTH]'].to_numpy()
z_velocity = ms_data['Vz(km/s)[J2000-EARTH]'].to_numpy()

test = np.array(x_velocity**2 + y_velocity**2 + z_velocity**2)

overall_velocity = np.array(np.sqrt(test))
scale_factor = 0.000125


def create_trajectory_line():
    points = [Vec3(x,y,z) * scale_factor for x, y, z in zip(ms_data['Rx(km)[J2000-EARTH]'],ms_data['Ry(km)[J2000-EARTH]'],ms_data['Rz(km)[J2000-EARTH]'])]

    line = Entity(model=Mesh(vertices=points, mode='line', thickness=2), color=color.red)
    return points, line

app = Ursina(size=(1000,500))

model = Entity(model='assets/textures-models/orion-models/orion3.obj', scale=(1, 1, 1), color=color.green)


index = 1

points, trajectory_line = create_trajectory_line()


editor_camera = EditorCamera(pan_speed = 1000)

camera.fov = 155

point_index = 0
overall_velocity = overall_velocity * 0.0005
speed = overall_velocity[0]
distance = 0

distancetotal = Text(text='Distance Traveled (km): '+str(distance),x=0.55,y=0.47,size=0.04)

def length(x,y,z,x2,y2,z2):
    x = x/0.000125
    y = y/0.000125
    z = z/0.000125
    x2 = x2/0.000125
    y2 = y2/0.000125
    z2 = z2/0.000125
    a = x2-x
    b = y2-y
    c = z2-z
    d = a**2 + b**2 + c**2
    return np.sqrt(d)

def update():

    global point_index, speed, points, distance
    # WASD camera movement
    if held_keys['w']: editor_camera.position += editor_camera.forward * time.dt * 5  # Move forward
    if held_keys['s']: editor_camera.position -= editor_camera.forward * time.dt * 5  # Move backward
    if held_keys['a']: editor_camera.position -= editor_camera.right * time.dt * 5    # Move left
    if held_keys['d']: editor_camera.position += editor_camera.right * time.dt * 5    # Move right
    if held_keys['q']: editor_camera.position += editor_camera.up * time.dt * 5       # Move up
    if held_keys['e']: editor_camera.position -= editor_camera.up * time.dt * 5       # Move down
    if held_keys["escape"]:
        quit()
    if point_index < len(points):
        model.position = points[point_index]
        speed = overall_velocity[point_index]
        x,y,z = points[point_index]
        x2,y2,z2 = points[point_index+1]
        distance += length(x,y,z,x2,y2,z2)
        distance = np.round(distance, 2)
        distancetotal.text = 'Distance Traveled (km): '+str(distance)
        point_index += int(speed * len(points))
    else:
        point_index = 0
        speed = overall_velocity[0]
        distance = 0

class Planet:
    def __init__(self, scale, file, pos=(0, 0, 0)):
        self.entity = Entity(model="sphere", texture=file, scale=(scale, scale, scale), position=pos)
earth = Planet(2, "assets/textures-models/planet-textures/earth.jpg").entity
moon = Planet(0.54, "assets/textures-models/planet-textures/moon.jpg", pos=(-384400 * scale_factor, -17, -5)).entity
earth.cull_faces, earth.double_sided = False, True
moon.cull_faces, moon.double_sided = False, True
space_bg = Sky(texture="assets/textures-models/space-textures/space4.jpg")


app.run()