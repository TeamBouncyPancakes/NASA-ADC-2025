import pandas as pd
from ursina import *
import numpy as np
from antenna_func import antenna_prioritize

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

model = Entity(model='assets/textures-models/orion-models/orion_service_module.obj', scale=(1, 1, 1), color=color.light_gray)
model2 = Entity(model='assets/textures-models/orion-models/orion_capsule_new.obj', scale=(1, 1, 1), color=color.light_gray)

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

antenna_models = [
    load_model("assets/textures-models/antenna-models/DSN_34.obj"),
    load_model("assets/textures-models/antenna-models/DSN_34_1.obj"),
    load_model("assets/textures-models/antenna-models/DSN_34_2.obj")
]

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
        model2.position = points[point_index]
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
earth = Planet(12742 * scale_factor, "assets/textures-models/planet-textures/earth.jpg").entity
moon = Planet(3474 * scale_factor, "assets/textures-models/planet-textures/moon.jpg", pos=((-384400 * scale_factor) + 1, -16.25, -8)).entity
earth.cull_faces, earth.double_sided = False, True
moon.cull_faces, moon.double_sided = False, True
space_bg = Sky(texture="assets/textures-models/space-textures/space4.jpg")

def lat_lon_to_3d(lat, lon, radius):
    """Convert latitude and longitude to 3D coordinates on a sphere."""
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    x = radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = radius * math.sin(lat_rad)
    z = radius * math.cos(lat_rad) * math.sin(lon_rad)
    return Vec3(x, y, z)


def place_marker(lat, lon, radius, color=color.white, scale=0.0005, parent=None, texture=None, model=load_model('assets/textures-models/antenna-models/DSN_34.obj')):
    """Place a marker at the specified latitude and longitude on the sphere."""
    position = lat_lon_to_3d(lat, lon, radius)  # Exact surface position
    marker = Entity(model=model, scale=scale, parent=parent, color=color, position=position, texture=texture)
    return marker


antenna_locations = [
    (35.3399, -116.875), # California
    (-35.5985, 148.982), # Australia
    (40.5276, -4.5271), # Spain
]

model_number = 0

for lat, lon in antenna_locations:
    place_marker(lat, lon, radius=0.5, color=color.white, scale=0.01, parent=earth, model=antenna_models[model_number])  # Attach antennas to Earth
    model_number += 1

def start():
    app.run()

start()