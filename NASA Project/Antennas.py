import numpy
from ursina import *
from PIL import Image
from math import sin, cos, radians
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader, unlit_shader
import pandas as pd
import time

app = Ursina()

camera = EditorCamera()

camera.fov = 155

point_index = 0
distance = 0

model_name = "DSN_34"
antenna = load_model(f'assets/textures-models/antenna-stuff/{model_name}.obj')

def input(key):
    if key == "escape" or key == "q":
        exit()
    earth.rotation_x += (held_keys['x'] * time.dt) * 1000
    earth.rotation_y += (held_keys['y'] * time.dt) * 1000
    move_speed = 10 * time.dt
    if held_keys['g']: camera.position += (move_speed, 0, 0)
    if held_keys['i']: camera.position -= (move_speed, 0, 0)
    if held_keys['h']: camera.position += (0, move_speed, 0)
    if held_keys['o']: camera.position -= (0, move_speed, 0)
    if held_keys['j']: camera.position += (0, 0, -move_speed)
    if held_keys['p']: camera.position -= (0, 0, -move_speed)

def update():
    # Rotate the Earth
    earth.rotation_y -= 1 * time.dt  # The Earth rotates on its Y-axis
    moon.rotation_y -= 0.0366 * time.dt

class Planet:
    def __init__(self, tripscale, file, pos=(0, 0, 0)):
        self.entity = Entity(model="sphere", texture=file, scale=(tripscale, tripscale, tripscale), position=pos)

def lat_lon_to_3d(lat, lon, radius):
    """Convert latitude and longitude to 3D coordinates on a sphere."""

    # Check if latitude is within the valid range
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees.")

    # Check if longitude is within the valid range
    if not (-180 <= lon <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    x = radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = radius * math.sin(lat_rad)
    z = radius * math.cos(lat_rad) * math.sin(lon_rad)
    return Vec3(x, y, z)

def place_marker(lat, lon, radius, color=color.white, scale=0.0005, parent=None, texture=None):
    """Place a marker at the specified latitude and longitude on the sphere."""
    position = lat_lon_to_3d(lat, lon, radius)  # Exact surface position
    marker = Entity(model=antenna, scale=scale, color=color, position=position, texture=texture, parent=earth)
    return marker

# Create the Earth and Moon
earth = Planet(2, "assets/textures-models/planet-textures/earth.jpg").entity
moon = Planet(0.54, "assets/textures-models/planet-textures/moon.jpg", pos=(60, 0, 0)).entity
earth.cull_faces, earth.double_sided = False, True
moon.cull_faces, moon.double_sided = False, True

# Editor camera

# Sky background
Sky(texture="assets/textures-models/space-textures/space4.jpg")

# Define the Earth's radius
earth_radius = 1.0  # The Earth's radius in your model is 1.0 unit (due to model scaling)

# Add Artemis II antenna markers (example latitudes and longitudes)
antenna_locations = [
    (35.3399, -116.875),  # CA
    (-35.5985, 148.982),  # Aus
    (40.5276, -4.5271),  # ESP


]

place_marker(35.3399, -116.875, radius=0.5, color=color.red, scale=0.006)
place_marker(-35.5985, 148.982, radius=0.5, color=color.red, scale=0.006)
place_marker(40.5276, -4.5271, radius=0.5, color=color.red, scale=0.006)

# Place markers on Earth and set them as children of the Earth entity, ensuring they touch the surface
mouse.locked = True



app.run()