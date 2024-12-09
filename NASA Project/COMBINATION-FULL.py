import numpy as np
from ursina import *
import pandas as pd
import time
from panda3d.core import FrameBufferProperties
# Renamed to avoid conflict with Ursina's Texture
from panda3d.core import Texture as p3dTexture
from csv_funcs import *
import platform
import os

os_ = platform.system()
if os_ == "Darwin":
    minimap = False
else:
    minimap = True

app = Ursina(size=(1000, 500))

ms_data = pd.read_csv("middle-school-data.csv")

x_velocity = ms_data['Vx(km/s)[J2000-EARTH]'].to_numpy()
y_velocity = ms_data['Vy(km/s)[J2000-EARTH]'].to_numpy()
z_velocity = ms_data['Vz(km/s)[J2000-EARTH]'].to_numpy()

times = ms_data['MISSION ELAPSED TIME (min)'].to_numpy()

test = np.array(x_velocity ** 2 + y_velocity ** 2 + z_velocity ** 2)

overall_velocity = np.array(np.sqrt(test))
scale_factor = 0.000125

colors = [color.red, color.cyan, color.green, color.gold, color.pink, color.yellow, color.orange, color.brown,
          color.azure, color.lime]

bg = Sprite(
    'assets/textures-models/space-textures/moonbg.jpg',
    scale=(1, 1),
    position=(1.75, 2.25, 10),
    parent=camera.ui
)  # background sprite image (moon background)

font_family = "SpaceMono-Regular.ttf"

menu_text = Text(
    text='NASA ADC 2025 Project',
    position=(-0.625, 0.4, -1),
    scale=2,
    font=f"assets/fonts/{font_family}"
)  # text for title

subtitle = Text(
    text='by Team Bouncy Pancakes',
    position=(-0.625, 0.345, -1),
    scale=1,
    color=color.gray,
    font=f"assets/fonts/{font_family}"
)  # subtitle text

play_text = Text(
    text='Artemis II Simulation',
    color=color.black,
    position=(-0.125, 0.1125, -1),
    font=f"assets/fonts/{font_family}"
)  # play simulation (text)
quit_text = Text(
    text='Quit Application',
    color=color.black,
    position=(-0.096875, -0.2875, -1),
    font=f"assets/fonts/{font_family}"
)  # quit simulation (text)
viewer_text = Text(
    text='Model Viewer',
    color=color.black,
    position=(-0.09375, -0.0875, -1),
    font=f"assets/fonts/{font_family}"
)  # view model (text)

play_button = Button(
    scale=(0.3, 0.1),
    position=(0, 0.1),
    color=color.white
)  # play button
play_button.highlight_color = color.gray
play_button.text_entity = play_text
play_button.on_click = (lambda: ui_off(manual=True))

quit_button = Button(
    scale=(0.3, 0.1),
    position=(0, -0.3),
    on_click=application.quit,
    color=color.white
)  # quit button
quit_button.highlight_color = color.gray
quit_button.text_entity = quit_text
quit_button.on_click = application.quit

viewer_button = Button(
    scale=(0.3, 0.1),
    position=(0, -0.1),
    color=color.white,
    on_click=lambda: os.system("python3 UI_modelpage.py")
)  # view models button
viewer_button.highlight_color = color.gray
viewer_button.text_entity = viewer_text

# button.highlight_color = color.gray
# button.text_entity = button_text
# First one - sets hover color to gray
# Second one - connects the text and button

logo = Sprite(
    'assets/other/logo.png',
    scale=(0.25, 0.25),
    position=(0.75, 3.5)
)  # Project team logo
ci = 0


def lerp(p1, p2, t):
    x = (1 - t) * p1
    y = p2 * t
    a = x + y
    return a


points = [Vec3(a, b, s) * 0.000125 for a, b, s in
          zip(ms_data['Rx(km)[J2000-EARTH]'], ms_data['Ry(km)[J2000-EARTH]'], ms_data['Rz(km)[J2000-EARTH]'])]


def create_trajectory_line(c, x, y):
    global ci, points  # Ensure 'points' is properly initialized and populated
    scale_factor = 0.000125

    # Validate 'points' list and indices
    if not points or len(points) <= max(x, y):
        print("Error: Invalid points list or indices out of range.")
        return None, None

    # Extract current points
    current = [points[x], points[y]]

    # Ensure points are valid Vec3 objects
    if not all(isinstance(pt, Vec3) for pt in current):
        print("Error: Points must be Vec3 objects.")
        return None, None

    # Create a line entity using the two points
    vertices = current  # Start and end points for the line
    line = Entity(
        model=Mesh(vertices=vertices, mode='line', thickness=2),  # Create a line model
        color=c,  # Optional scaling
    )

    # print('Drew line.')

    return line, current


index = 1

trajectory_line, current = create_trajectory_line(colors[ci], 0, 1)

editor_camera = EditorCamera(pan_speed=1000)
# app.run()


point_index = 0
overall_velocity = overall_velocity * 0.001
speed = overall_velocity[0]
distance = 0
phase = "None"

distanceup = Text(text="Distance Travelled (km):", x=-0.97, y=0.37, size=0.02,
                  font='assets/fonts/SpaceMono-Regular.ttf')
distancetotal = Text(text=str(distance), x=-0.97, y=0.33, size=0.04, font='assets/fonts/SpaceMono-Regular.ttf')
distancetotal._eternal = True
distanceup._eternal = True

distanceup.alpha = 0
distancetotal.alpha = 0

phaseup = Text(text='Phase:', x=-0.97, y=0.47, size=0.02, font='assets/fonts/SpaceMono-Regular.ttf')
phaselabel = Text(text=phase, x=-0.97, y=0.43, size=0.04, font='assets/fonts/SpaceMono-Regular.ttf')
phaselabel._eternal = True
phaseup._eternal = True

phaseup.alpha = 0
phaselabel.alpha = 0

timeup = Text(text="Time (min):", x=-0.97, y=0.27, size=0.02, font='assets/fonts/SpaceMono-Regular.ttf')
timelabel = Text(text=str(times[0]), x=-0.97, y=0.23, font='assets/fonts/SpaceMono-Regular.ttf', size=0.04)
timelabel._eternal = True
timeup._eternal = True

timeup.alpha = 0
timelabel.alpha = 0

wh = Entity(model='quad', color=color.white, scale=(0.1, 0.1), position=(-0.6, 0.1), parent=camera.ui)

wh.alpha = 0

key1 = Text(text="Color Key (Phases):", x=-0.97, y=0.15, size=0.02, font='assets/fonts/SpaceMono-Regular.ttf')

key1.alpha = 0

key2a = Text(text="Launch:", x=-0.97, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key2b = Entity(model='quad', color=color.red, scale=(0.075, 0.075), position=(-0.6, 0.1), parent=camera.ui)

key2a.alpha = 0
key2b.alpha = 0

key3a = Text(text="Initital Firing:", x=-0.97, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key3b = Entity(model='quad', color=color.cyan, scale=(0.075, 0.075), position=(-0.6, 0.1), parent=camera.ui)

key3a.alpha = 0
key3b.alpha = 0

key4a = Text(text="Orion Separation:", x=-0.97, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key4b = Entity(model='quad', color=color.green, scale=(0.075, 0.075), position=(-0.6, 0.1), parent=camera.ui)

key4a.alpha = 0
key4b.alpha = 0

key5a = Text(text="Subsequent Burning:", x=-0.97, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key5b = Entity(model='quad', color=color.gold, scale=(0.075, 0.075), position=(-0.6, 0.1), parent=camera.ui)

key5a.alpha = 0
key5b.alpha = 0

key6a = Text(text="Life Systems Check:", x=-0.97, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key6b = Entity(model='quad', color=color.pink, scale=(0.075, 0.075), position=(-0.6, 0.1), parent=camera.ui)

key6a.alpha = 0
key6b.alpha = 0

key7a = Text(text="Burn Fuel:", x=-0.97, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key7b = Entity(model='quad', color=color.yellow, scale=(0.075, 0.075), position=(-0.6, 0.1), parent=camera.ui)

key7a.alpha = 0
key7b.alpha = 0

key8a = Text(text="Translunar Injection:", x=-0.97, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.02)
key8b = Entity(model='quad', color=color.orange, position=(-0.6, 0.1), scale=(0.075, 0.075), parent=camera.ui)

key8a.alpha = 0
key8b.alpha = 0

key9a = Text(text="Translunar Outbound:", x=-0.97, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key9b = Entity(model='quad', color=color.brown, scale=(0.075, 0.075), position=(-0.6, 0.1), parent=camera.ui)

key9a.alpha = 0
key9b.alpha = 0

key0a = Text(text="Return:", x=-0.97, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key0b = Entity(model='quad', color=color.azure, scale=(0.075, 0.075), position=(-0.6, 0.1), parent=camera.ui)

key0a.alpha = 0
key0b.alpha = 0

key15a = Text(text="Landing:", x=-0.97, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key15b = Entity(model='quad', color=color.lime, scale=(0.075, 0.075), position=(-0.6, 0.1), parent=camera.ui)

key15a.alpha = 0
key15b.alpha = 0

keys = {key2a: key2b, key3a: key3b, key4a: key4b, key5a: key5b, key6a: key6b, key7a: key7b, key8a: key8b, key9a: key9b,
        key0a: key0b, key15a: key15b}

## POSSIBLE USE FOR DEBUG
# xlabel = Text(text="X: "+str(points[0][0]/0.000125),x=-0.75,y=0.47)
# xlabel._eternal = True
# ylabel = Text(text="Y: "+str(points[0][1]/0.000125),x=-0.75,y=0.4)
# ylabel._eternal = True
# zlabel = Text(text="Z: "+str(points[0][2]/0.000125),x=-0.75,y=0.34)
# zlabel._eternal = True

distances = []


# antennas = antennas = [{'name':'WPSA','value':1000,'color':color.red},{'name':'DS54','value':800,'color':color.azure},{'name':'DS24','value':600,'color':color.green},{'name':'DS34','value':400,'color':color.orange}]

#
# antennatitle = Text(text="Antenna priority", x=0.97, y=0, size=0.02, font='assets/fonts/SpaceMono-Regular.ttf')
#
# antenna1 = Text(text="1) " + antennas[0]['name'] + " - " + str(antennas[0]['value']), x=0.9, y=-0.05, size=0.04,
#                 font='assets/fonts/SpaceMono-Regular.ttf', color=antennas[0]['color'])
#
# antenna2 = Text(text="2) " + antennas[1]['name'] + " - " + str(antennas[1]['value']), x=0.9, y=-0.1, size=0.04,
#                 font='assets/fonts/SpaceMono-Regular.ttf', color=antennas[1]['color'])
#
# antenna3 = Text(text="3) " + antennas[2]['name'] + " - " + str(antennas[2]['value']), x=0.9, y=-0.15, size=0.04,
#                 font='assets/fonts/SpaceMono-Regular.ttf', color=antennas[2]['color'])
#
# antenna4 = Text(text="4) " + antennas[3]['name'] + " - " + str(antennas[3]['value']), x=0.9, y=-0.2, size=0.04,
#                 font='assets/fonts/SpaceMono-Regular.ttf', color=antennas[3]['color'])


# p_b = Button(icon='playbutton.png', scale=.25, x=0, y=-0.4, color=color.white)
# p_b.alpha = 0


def length(x, y, z, x2, y2, z2):
    x = x / 0.000125
    y = y / 0.000125
    z = z / 0.000125
    x2 = x2 / 0.000125
    y2 = y2 / 0.000125
    z2 = z2 / 0.000125
    a = x2 - x
    b = y2 - y
    c = z2 - z
    d = a ** 2 + b ** 2 + c ** 2
    return np.sqrt(d)


antenna_models = [
    load_model("assets/textures-models/antenna-models/DSN_34.obj"),
    load_model("assets/textures-models/antenna-models/DSN_34_1.obj"),
    load_model("assets/textures-models/antenna-models/DSN_34_2.obj")
]


def clean_line(current, next, f):
    x = lerp(current.x, next.x, f)
    y = lerp(current.y, next.y, f)
    z = lerp(current.z, next.z, f)

    return Vec3(x, y, z)


ui_visible = False

inter = 0.75


class Planet:
    def __init__(self, scale, file, pos=(0, 0, 0)):
        self.entity = Entity(model="sphere", texture=file, scale=(scale, scale, scale), position=pos)


earth = Planet(12742 * scale_factor, "assets/textures-models/planet-textures/earth.jpg").entity
moon = Planet(3474 * scale_factor, "assets/textures-models/planet-textures/moon.jpg",
              pos=((-384400 * scale_factor) + 1, -16.25, -8)).entity
earth.cull_faces, earth.double_sided = False, True
moon.cull_faces, moon.double_sided = False, True
space_bg = Sky(texture="assets/textures-models/space-textures/space4.jpg")

antenna_locations = [
    (35.3399, -116.875),  # California
    (-35.5985, 148.982),  # Australia
    (40.5276, -4.5271),  # Spain
    (106.5364, 32.7804)
]

earth_radius = 1.0  # The Earth's radius in your model is 1.0 unit (due to model scaling)


def lat_lon_to_3d(lat, lon, radius):
    """Convert latitude and longitude to 3D coordinates on a sphere."""
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    x = radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = radius * math.sin(lat_rad)
    z = radius * math.cos(lat_rad) * math.sin(lon_rad)
    return Vec3(x, y, z)


antenna_models = [
    load_model('assets/textures-models/antenna-models/DSN_34.obj'),
    load_model('assets/textures-models/antenna-models/DSN_34_1.obj'),
    load_model('assets/textures-models/antenna-models/DSN_34_2.obj'),
    load_model('assets/textures-models/antenna-models/DSN_34_3.obj'),

]

camera.fov = 100


class marker:
    def __init__(self, position=(0, 0, 0), color=color.white, scale=0.0005, parent=None, texture=None,
                 model=load_model('assets/textures-models/antenna-stuff/Antenna_model')):
        self.pos = position
        self.color = color
        self.scale = scale
        self.parent = parent
        self.texture = texture
        self.model = model

    @property
    def entity(self):
        entity = Entity(color=self.color, scale=self.scale, parent=self.parent, texture=self.texture, model=self.model,
                        position=self.pos)

        return entity

    def update(self):
        self.entity.look_at(camera)


position = lat_lon_to_3d(antenna_locations[2][0], antenna_locations[2][1], earth_radius * 0.5)
texture = None
SpainMarker = marker(model=antenna_models[0], scale=0.001, parent=earth, color=color.red, position=position,
                     texture=texture)
SpainMarker.entity.show()

position = lat_lon_to_3d(antenna_locations[0][0], antenna_locations[0][1], earth_radius * 0.5)
texture = None
CAMarker = marker(model=antenna_models[1], scale=0.001, parent=earth, color=color.red, position=position,
                  texture=texture)
CAMarker.entity.show()

position = lat_lon_to_3d(antenna_locations[1][0], antenna_locations[1][1], earth_radius * 0.5)
texture = None
AustraliaMarker = marker(model=antenna_models[2], scale=0.001, parent=earth, color=color.red, position=position,
                         texture=texture)
AustraliaMarker.entity.show()

position = lat_lon_to_3d(antenna_locations[3][0], antenna_locations[3][1], earth_radius * 0.5)
texture = None
WPSA = marker(model=antenna_models[3], scale=0.001, parent=earth, color=color.red, position=position, texture=texture)
WPSA.entity.show()

antennas = [SpainMarker, CAMarker, AustraliaMarker, WPSA]
CAMarker.entity.rotate((305, 45, 15), earth)
SpainMarker.entity.rotate((385, 45, 40), earth)
AustraliaMarker.entity.rotate((310, 200, 90), earth)
WPSA.entity.rotate((45, 300, 30), earth)
model_number = 1

if minimap:
    properties = FrameBufferProperties()
    properties.set_rgb_color(True)
    properties.set_rgba_bits(80, 8, 8, 8)
    properties.set_depth_bits(12)
    # Setup the texture to be rendered into.
    render_texture = p3dTexture()
    render_texture.set_format(p3dTexture.F_rgba32)
    render_texture.set_component_type(p3dTexture.T_float)
    # Make the buffer, if size is set to (0, 0), then it matches the window size.
    render_buffer = app.win.make_texture_buffer('render', 512, 2048, render_texture, False, properties)
    # Determines in what order rendering happens, you can pick any integer, see Panda3D render ordering.
    # Negative means before the rest of the normal scene is drawn.
    render_buffer.set_sort(-100)

    camera_pos = Entity(model="cube", position=(0, 10, 0), color=color.olive)
    camera_pos.hide()
    # New camera that copies the lens from the Ursina default camera,
    # and is rendering scene (all Ursina entities are attached to scene by default).
    render_camera = app.make_camera(render_buffer, lens=camera.lens, scene=scene)
    # render_camera.NodePath.
    render_camera.reparentTo(camera_pos)
    # To display the results of the render texture.
    minimap_texture = Texture(render_texture)

    outline = Entity(model="quad", parent=camera.ui, scale=0.41, texture="assets/minimap-stuffs/outline-bg.jpg",
                     position=(0, 2, 0))

    minimapbg = Entity(model="quad", parent=camera.ui, scale=0.4,
                       texture="assets/textures-models/space-textures/space4.jpg",
                       position=(0, 2, 0))

    quad = Entity(model='quad', texture=minimap_texture, parent=camera.ui, scale=0.4)
    # bg.always_on_top = False
    quad.always_on_top = True

ui_objs = [logo, viewer_button, quit_button, play_button, viewer_text, play_text, quit_text, subtitle, menu_text, bg]
if minimap:
    ui_objs.append(minimapbg)
    ui_objs.append(quad)
non_ui = [trajectory_line, earth, moon, space_bg]
for antenna in antennas:
    non_ui.append(antenna)

model_number = 0


def ui_on(manual=False):
    global ui_visible
    for obj in non_ui:
        obj.visible = False
    for ui in ui_objs:
        ui.visible = True
    ui_visible = True
    # print("UI on") if not manual else print("FORCE BUTTON UI ON")


def ui_off(manual=False):
    global ui_visible
    for obj in non_ui:
        obj.visible = True
    for ui in ui_objs:
        ui.visible = False
    ui_visible = False
    # print("UI off") if not manual else print("FORCE BUTTON UI OFF")


ui_on()

# loading orion modules
slsbody = load_model('assets/textures-models/orion-models/orion_nasa_sls_body.glb')
slsbody_entity = Entity(model=slsbody, scale=(0.12, 0.12, 0.12))
slsbody_entity.rotation_z = 180
slsbody_entity.y = 0.45
slsnose = load_model('assets/textures-models/orion-models/orionmpcv.glb')
slsnose_entity = Entity(model=slsnose, scale=(0.12, 0.12, 0.12))
slsnose_entity.y = 10
icps = load_model('assets/textures-models/orion-models/icpstextured.glb')
service_module = load_model('assets/textures-models/orion-models/servicemoduletextured.glb')
capsule = load_model('assets/textures-models/orion-models/orioncapsuletextured.glb')
capsule_entity = Entity(model=capsule, position=(-1.7, 3.21, -0.18))
service_module_entity = Entity(model=service_module, scale=1, position=(-3.5, 1.2, 0))
orion = Entity(scale=(0.2, 0.2, 0.2))
orion.position = (0, 0, 0)
capsule_entity.parent = orion
service_module_entity.parent = orion
icps_entity = Entity(model=icps, scale=0.008, position=(-0.33, 0.3, 0))
icps_entity.rotation_x = -90
orion_maste = Entity(scale=(1, 1, 1))
icps_entity.parent = orion_maste
orion.parent = orion_maste
# sls.parent = orion_maste   
orion_maste.y = 9.8
orion_maste.x = 0.33
g_scale = 0.2
orion_master = Entity(scale=(g_scale, g_scale, g_scale))
slsbody_entity.parent = orion_master
slsnose_entity.parent = orion_master
orion_maste.parent = orion_master
# orion_master.z = -0.5
slsbody_entity.rotation_y = 90
orion_master.rotation_z = -90
light = DirectionalLight(parent=orion_master)
light.look_at(orion_master)


def median_filter(points, window_size=3):
    smoothed_points = []
    for i in range(len(points)):
        # Define the window range: from max(0, i - window_size//2) to min(len(points), i + window_size//2)999
        start = max(0, i - window_size // 2)
        end = min(len(points), i + window_size // 2 + 1)

        # Extract the window of points
        window = points[start:end]

        # Apply median filter to each dimension (x, y, z)
        window_x = [p[0] for p in window]
        window_y = [p[1] for p in window]
        window_z = [p[2] for p in window]

        # Calculate the median for each dimension
        median_x = np.median(window_x)
        median_y = np.median(window_y)
        median_z = np.median(window_z)

        # Create a new smoothed point using the median values
        smoothed_point = Vec3(median_x, median_y, median_z)
        smoothed_points.append(smoothed_point)

    return smoothed_points


points_array = median_filter(points, 30)


# points = points_array

def separate(e1, e2):
    e1.parent = None
    e2.parent = None


def translate_orion(e, x, y, z):
    e.x += x
    e.y += y
    e.z += z


ambient_light = AmbientLight()
ambient_light.intensity = 0.5

print(camera.position)


def update():

    if ui_visible:
        editor_camera.enabled = False
        editor_camera.position = (0, 0, -10)
        editor_camera.rotation = (0, 0, 0)
        ui_on()
    else:
        editor_camera.enabled = True
        ui_off()

    global point_index, speed, points, distance, ci, pi, distances, phase, times, trajectory_line, model, current, inter, h
    o = list(keys.items())
    # WASD camera movement
    if held_keys['w']: editor_camera.position += editor_camera.forward * time.dt * 5  # Move forward
    if held_keys['s']: editor_camera.position -= editor_camera.forward * time.dt * 5  # Move backward
    if held_keys['a']: editor_camera.position -= editor_camera.right * time.dt * 5  # Move left
    if held_keys['d']: editor_camera.position += editor_camera.right * time.dt * 5  # Move right
    if held_keys['q']: editor_camera.position += editor_camera.up * time.dt * 5  # Move up
    if held_keys['e']: editor_camera.position -= editor_camera.up * time.dt * 5  # Move down
    if held_keys["escape"]:
        quit()

    if point_index < len(points):
        currents = points[point_index + 2]
        previous = points[point_index]
        if point_index + 1 == len(points):
            next = points[0]
        else:
            next = points[point_index + 1]

        # intergrating orion onto trajectory
        direction = (currents - previous).normalized()
        orion_master.position += direction * 1 * time.dt

        if direction.length() > 0:
            # Calculate the angle in radians
            target_rotation_y = math.degrees(math.atan2(direction.x, direction.y))
            orion_master.rotation_y = lerp(orion_master.rotation_y, target_rotation_y, 5 * time.dt)

            # Update the front's orientation to match the direction of movement
            tp = orion_master.position + direction
            orion_master.look_at(tp)
            if orion_master.rotation_y > 0:
                orion_master.rotation_y += 90
            else:
                orion_master.rotation_y -= 90

        if 8 <= times[point_index] < 48.23658:
            ci = 0
            key2a.alpha = 1
            key2b.alpha = 1
        elif 48.23658 <= float(times[point_index]) < 100.1082:
            ci = 1
            phase = "Initial firing"
            m, j = o[ci]
            m.alpha = 1
            j.alpha = 1
            k, i = o[ci - 1]
            k.alpha = 0
            i.alpha = 0
        elif 100.1082 <= float(times[point_index]) < 196.0945:
            ci = 2
            phase = "Orion separates from ICPS"
            m, j = o[ci]
            m.alpha = 1
            j.alpha = 1
            k, i = o[ci - 1]
            k.alpha = 0
            i.alpha = 0
        elif 196.0945 <= float(times[point_index]) < 283.6495:
            ci = 3
            phase = "Subsequent burning of fuel for higher orbit"
            m, j = o[ci]
            m.alpha = 1
            j.alpha = 1
            k, i = o[ci - 1]
            k.alpha = 0
            i.alpha = 0
        elif 283.6495 <= float(times[point_index]) < 792.4494:
            ci = 4
            phase = "Life Systems Check/Orion USS Burn"
            m, j = o[ci]
            m.alpha = 1
            j.alpha = 1
            k, i = o[ci - 1]
            k.alpha = 0
            i.alpha = 0
        elif 792.4494 <= float(times[point_index]) < 1487.65:
            ci = 5
            phase = "Life Systems Check/Burn Fuel"
            m, j = o[ci]
            m.alpha = 1
            j.alpha = 1
            k, i = o[ci - 1]
            k.alpha = 0
            i.alpha = 0
        elif 1487.65 <= float(times[point_index]) < 6150.25142:
            ci = 6
            phase = "TransLunar Injection Propells to Moon"
            m, j = o[ci]
            m.alpha = 1
            j.alpha = 1
            k, i = o[ci - 1]
            k.alpha = 0
            i.alpha = 0
        elif 6150.25142 <= float(times[point_index]) < 7200.25142:
            ci = 7
            phase = 'Translunar Outbound'

            m, j = o[ci]
            m.alpha = 1
            j.alpha = 1
            k, i = o[ci - 1]
            k.alpha = 0
            i.alpha = 0
        elif 7200.25142 <= float(times[point_index]) < 10150.16998:
            ci = 8
            phase = 'Return to Earth'
            m, j = o[ci]
            m.alpha = 1
            j.alpha = 1
            k, i = o[ci - 1]
            k.alpha = 0
            i.alpha = 0
        elif 12690 <= float(times[point_index]):
            ci = 9
            phase = 'Landing'
            m, j = o[ci]
            m.alpha = 1
            j.alpha = 1
            k, i = o[ci - 1]
            k.alpha = 0
            i.alpha = 0

        if len(points) != point_index + 1:
            h = times[point_index + 1] - times[point_index]
            h *= 60
            h = h / 25960.633996

        if ci >= 2:
            separate(slsnose_entity, slsbody_entity)
            slsnose_entity.z -= 0.5
            slsbody_entity.z -= 0.5
            orion_maste.position = Vec3(0, 0, 0)

        if ci >= 6:
            icps_entity.parent = None
            icps_entity.z -= 0.5
            orion_maste.position = Vec3(0, 0, 0)

        if ci >= 9:
            orion_capsule.parent = None
            orion_capsule.z -= 0.5
            orion_maste.position = Vec3(0, 0, 0)

        # xlabel.text="X: "+str(round(points[point_index][0],5)/0.000125)
        # ylabel.text="Y: "+str(round(points[point_index][1],5)/0.000125)
        # zlabel.text="Z: "+str(round(points[point_index][2],5)/0.000125)

        # print('Completed')
        # print(ci)
        if ui_visible:
            pass
        else:
            wh.alpha = 1
            distanceup.alpha = 1
            distancetotal.alpha = 1
            phaseup.alpha = 1
            phaselabel.alpha = 1
            timeup.alpha = 1
            timelabel.alpha = 1
            key1.alpha = 1
            orion_master.position = Vec3(currents.x, currents.y, currents.z)  # clean_line(currents, next, inter)
            speed = overall_velocity[point_index]
            x, y, z = orion_master.position
            x2, y2, z2 = next

            current.append(points[point_index + 1])

            distance += length(x, y, z, x2, y2, z2)
            distance = np.round(distance, 2)
            distances.append(distance)
            if point_index + 1 != len(points):
                a = Mesh(vertices=current, mode='line', thickness=2)
                trajectory_line.model = a
            #        else:
            #            point_index = 0
            #  trajectory_line.alpha = 0
            distancetotal.text = str(distance)
            timelabel.text = str(float(times[point_index]))
            phaselabel.text = phase
            trajectory_line, current = create_trajectory_line(colors[ci], point_index, point_index + 1)
            inter += speed * time.dt
            time.sleep(h)
            point_index += int(speed * len(points) / 5.3)
            if inter >= 1.0:
                inter = 0
                point_index += 1
        # point_index += int(speed*len(points)/5.301)


    else:
        point_index = 0
        speed = overall_velocity[0]
        distance = 0
        current = [points[0], points[1]]
        # scene.clear()
    if os == "Darwin":
        minimap = False
    else:
        minimap = True
        if ui_visible:
            minimap = False
        else:
            minimap = True
    global n
    n += 1
    # bg_for_circle_identifier.x = window.top_left.x + bg_for_circle_identifier.scale.x * 0.5
    # bg_for_circle_identifier.y = window.top_left.y - bg_for_circle_identifier.scale.y * 0.5
    #
    # prioritization_circle_identifier.x = window.top_left.x + prioritization_circle_identifier.scale.x * 0.5
    # prioritization_circle_identifier.y = window.top_left.y - prioritization_circle_identifier.scale.y * 0.5
    if minimap:
        quad.x = window.bottom_right.x - quad.scale.x * 0.5

        quad.y = window.bottom_right.y + quad.scale.y * 0.5
        bg.x = window.bottom_right.x - bg.scale.x * 0.5
        bg.y = window.bottom_right.y + bg.scale.y * 0.5
        outline.x = window.bottom_right.x - outline.scale.x * 0.5
        outline.y = window.bottom_right.y + outline.scale.y * 0.5

    none_active = "None active"
    assets_prefix = "assets/antenna-prioritization/"
    neutral_png = assets_prefix + "neutral.png"

    # if not toggle:
    #     if csv_to_antenna(n) != none_active:
    #         prioritization_circle_identifier.texture = str(assets_prefix + str(csv_to_antenna(n)) + ".png")
    #     else:
    #         prioritization_circle_identifier.texture = neutral_png
    # else:
    #     should_look = look_forwards(10, n)
    #     if should_look != none_active:
    #         prioritization_circle_identifier.texture = str(assets_prefix + str(should_look) + ".png")
    #     else:
    #         prioritization_circle_identifier.texture = neutral_png


def start():
    app.run()


n = 0

try:
    start()


except Exception as e:
    print(e, "ERRRRRRRRRROEEEEEEEE")

