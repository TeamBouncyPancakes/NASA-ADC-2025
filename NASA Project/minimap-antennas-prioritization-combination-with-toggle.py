import numpy
import csv
from ursina import *
from PIL import Image
from math import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader, unlit_shader
import pandas as pd
from PIL import ImageGrab
#from InitUi import *
import time
from panda3d.core import FrameBufferProperties
# Renamed to avoid conflict with Ursina's Texture
from panda3d.core import Texture as p3dTexture
from ursina.shaders import *
from ursina.camera import Camera
from csv_location_finder_functions import *

app = Ursina(size=(800, 600))
box = Entity(model='cube', texture='Hackathon/waves.png')

#ed = EditorCamera()

toggle = True
def take_screenshot():
    screenshot = ImageGrab.grab()  # Capture the screen
    screenshot.save('screenshot.png')  # Save with the same name
    print("Screenshot taken!")  # Optional feedback in console

cam = FirstPersonController(gravity=0)

def input(key):
    if key == "escape" or key == "q":
        exit()
    earth.rotation_x += (held_keys['x'] * time.dt) * 1000
    earth.rotation_y += (held_keys['y'] * time.dt) * 1000
    move_speed = 10 * time.dt
    if held_keys['g']: cam.position += (move_speed, 0, 0)
    if held_keys['i']: cam.position -= (move_speed, 0, 0)
    if held_keys['h']: cam.position += (0, move_speed, 0)
    if held_keys['o']: cam.position -= (0, move_speed, 0)
    if held_keys['j']: cam.position += (0, 0, -move_speed)
    if held_keys['p']: cam.position -= (0, 0, -move_speed)

def update():
    # Rotate the Earth
    earth.rotation_y -= 1 * time.dt  # The Earth rotates on its Y-axis
    moon.rotation_y -= 0.0366 * time.dt

class Planet:
    def __init__(self, tripscale, file, pos=(0, 0, 0)):
        self.entity = Entity(model="sphere", texture=file, scale=(tripscale,tripscale,tripscale), position=pos)

class marker:
    def __init__(self, position=(0,0,0), color=color.white, scale=0.0005, parent=None, texture=None, model=load_model('assets/textures-models/antenna-stuff/Antenna_model')):
        self.pos = position
        self.color = color
        self.scale = scale
        self.parent = parent
        self.texture = texture
        self.model = model

    @property
    def entity(self):
        entity = Entity(color=self.color, scale=self.scale, parent=self.parent, texture=self.texture, model=self.model, position=self.pos)

        return entity

    def update(self):
        self.entity.look_at(cam)


def lat_lon_to_3d(lat, lon, radius):
    """Convert latitude and longitude to 3D coordinates on a sphere."""
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    x = radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = radius * math.sin(lat_rad)
    z = radius * math.cos(lat_rad) * math.sin(lon_rad)
    return Vec3(x, y, z)







# Create the Earth and Moon
earth = Planet(2, "assets/textures-models/planet-textures/earth.jpg", pos=(0,2,0)).entity
moon = Planet(0.54, "assets/textures-models/planet-textures/moon.jpg", pos=(60, 0, 0)).entity
earth.cull_faces, earth.double_sided = False, True
moon.cull_faces, moon.double_sided = False, True


# Sky background
Sky(texture="assets/textures-models/space-textures/space4.jpg")

# Define the Earth's radius
earth_radius = 1.0  # The Earth's radius in your model is 1.0 unit (due to model scaling)

# Add Artemis II antenna markers (example latitudes and longitudes)
antenna_locations = [
    (35.3399, -116.875), # California
    (-35.5985, 148.982), # Australia
    (40.5276, -4.5271), # Spain
]

antenna_models = [
    load_model('assets/textures-models/antenna-stuff/Antenna_model'),
    load_model('assets/textures-models/antenna-stuff/Antenna_model1'),
    load_model('assets/textures-models/antenna-stuff/Antenna_model2'),

]


position = lat_lon_to_3d(antenna_locations[2][0], antenna_locations[2][1], earth_radius*0.5)
texture = None
SpainMarker = marker(model=antenna_models[0], scale=0.001, parent=earth, color=color.red, position=position, texture=texture)
SpainMarker.entity.show()

position = lat_lon_to_3d(antenna_locations[0][0], antenna_locations[0][1], earth_radius*0.5)
texture = None
CAMarker = marker(model=antenna_models[1], scale=0.001, parent=earth, color=color.red, position=position, texture=texture)
CAMarker.entity.show()
mouse.locked = True


CAMarker.entity.rotate((305,45,15),earth)
SpainMarker.entity.rotate((385,45,40),earth)


player = FirstPersonController(gravity=0)

cam3 = Camera()

# Specify what type of buffer we want.
properties = FrameBufferProperties()
properties.set_rgb_color(True)
properties.set_rgba_bits(80, 8, 8, 8)
properties.set_depth_bits(12)
# Setup the texture to be rendered into.
render_texture = p3dTexture()
render_texture.set_format(p3dTexture.F_rgba32)
#render_texture.set_component_type(p3dTexture.T_float)
# Make the buffer, if size is set to (0, 0), then it matches the window size.
render_buffer = app.win.make_texture_buffer('render', 512, 2048, render_texture, False, properties)
# Determines in what order rendering happens, you can pick any integer, see Panda3D render ordering.
# Negative means before the rest of the normal scene is drawn.
render_buffer.set_sort(-100)

camera_pos = Entity(model="cube", position=(0,10,0), color=color.olive)
# New camera that copies the lens from the Ursina default camera,
# and is rendering scene (all Ursina entities are attached to scene by default).
render_camera = app.make_camera(render_buffer, lens=camera.lens, scene=scene)
#render_camera.NodePath.
# Make it follow Ursina's camera.
render_camera.reparentTo(camera_pos)
# To display the results of the render texture.
tex = Texture(render_texture)

outline = Entity(model="quad", parent=camera.ui, scale=0.41, texture="assets/minimap-stuffs/outline-bg.jpg  ", position=(0,2,0))

bg = Entity(model="quad", parent=camera.ui, scale=0.4, texture="assets/textures-models/space-textures/space4.jpg", position=(0,2,0))

quad = Entity(model='quad', texture=tex, parent=camera.ui, scale=0.4)
bg.always_on_top = True
#bg.always_on_top = False
quad.always_on_top = True
mouse.locked = True

render_camera.look_at(earth)


prioritization_circle_identifier = Entity(model='quad', texture="assets/antenna-prioritization/neutral2.png", parent=camera.ui, scale=0.2)
bg_for_circle_identifier = Entity(model='quad', texture="assets/antenna-prioritization/bg.png", parent=camera.ui, scale=0.21)

prioritization_circle_identifier.always_on_top = True
#prioritization_circle_identifier.reparentTo(camera)
#camera_pos.visible = False
n = 0
def update():
    global n
    n += 1
    time.sleep(0.01)
    if held_keys['escape']:
        application.quit()
    if held_keys['shift']:
        player.y -= 0.2
    if held_keys['space']:
        player.y += 0.2
    if held_keys['o']:
        take_screenshot()

    bg_for_circle_identifier.x = window.top_left.x + bg_for_circle_identifier.scale.x * 0.5
    bg_for_circle_identifier.y = window.top_left.y - bg_for_circle_identifier.scale.y * 0.5

    prioritization_circle_identifier.x = window.top_left.x + prioritization_circle_identifier.scale.x * 0.5
    prioritization_circle_identifier.y = window.top_left.y - prioritization_circle_identifier.scale.y * 0.5
    quad.x = window.bottom_right.x - quad.scale.x * 0.5
    quad.y = window.bottom_right.y + quad.scale.y * 0.5
    bg.x = window.bottom_right.x - bg.scale.x * 0.5
    bg.y = window.bottom_right.y + bg.scale.y * 0.5
    outline.x = window.bottom_right.x - outline.scale.x * 0.5
    outline.y = window.bottom_right.y + outline.scale.y * 0.5
    cam.look_at(box)
    cam.position = (25,0,0)

    none_active = "None active"
    assets_prefix = "assets/antenna-prioritization/"
    neutral_png = assets_prefix + "neutral.png"

    if not toggle:
        print(csv_to_antenna(n))
        if csv_to_antenna(n) != none_active:
            prioritization_circle_identifier.texture = str(assets_prefix + str(csv_to_antenna(n)) + ".png")
        else:
            prioritization_circle_identifier.texture = neutral_png
    else:
        should_look = look_forwards(10, n)
        print(should_look)
        if should_look != none_active:
            prioritization_circle_identifier.texture = str(assets_prefix + str(should_look) + ".png")
        else:
            prioritization_circle_identifier.texture = neutral_png


app.run()