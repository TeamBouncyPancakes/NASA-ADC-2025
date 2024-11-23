import numpy as np
import pandas as pd
from ursina import *

app = Ursina(size=(1000, 500))

ms_data = pd.read_csv('middle-school-data.csv')

x_velocity = ms_data['Vx(km/s)[J2000-EARTH]'].to_numpy()
y_velocity = ms_data['Vy(km/s)[J2000-EARTH]'].to_numpy()
z_velocity = ms_data['Vz(km/s)[J2000-EARTH]'].to_numpy()

times = ms_data['MISSION ELAPSED TIME (mins)'].to_numpy()

test = np.array(x_velocity ** 2 + y_velocity ** 2 + z_velocity ** 2)

overall_velocity = np.array(np.sqrt(test))
scale_factor = 0.000125

colors = [color.red, color.cyan, color.green, color.gold, color.pink, color.yellow, color.blue, color.brown,
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
    color=color.white
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
    global ci, points
    scale_factor = 0.000125

    current = [points[x], points[y]]
    line = Entity(model=Mesh(vertices=points, mode='line', thickness=2), color=c)
    return line, current



service_module = Entity(model='assets/textures-models/orion-models/orion_service_module.obj', scale=(1, 1, 1),
                        color=color.light_gray)
model = Entity(model='assets/textures-models/orion-models/orion_capsule_new.obj', scale=(1, 1, 1),
                 color=color.light_gray)
capsule = model

capsule_entity = Entity(model=capsule, position=(0, 0, 0))
service_module_entity = Entity(model=service_module, scale=1, position=(0, 1.2, 0))

orion = Entity(scale=(0.3, 0.3, 0.3))
orion.position = (0, 0, 0)

capsule_entity.parent = orion
service_module_entity.parent = orion

index = 1

trajectory_line, current = create_trajectory_line(colors[ci], 0, 1)

editor_camera = EditorCamera(pan_speed=1000)

camera.fov = 155

point_index = 0
overall_velocity = overall_velocity * 0.001
speed = overall_velocity[0]
distance = 0
phase = "Launch"

distanceup = Text(text="Distance Travelled (km):", x=-1.2, y=0.37, size=0.02, font='assets/fonts/SpaceMono-Regular.ttf')
distancetotal = Text(text=str(distance), x=-1.2, y=0.33, size=0.04, font='assets/fonts/SpaceMono-Regular.ttf')
distancetotal._eternal = True
distanceup._eternal = True

phaseup = Text(text='Phase:', x=-1.2, y=0.47, size=0.02, font='assets/fonts/SpaceMono-Regular.ttf')
phaselabel = Text(text=phase, x=-1.2, y=0.43, size=0.04, font='assets/fonts/SpaceMono-Regular.ttf')
phaselabel._eternal = True
phaseup._eternal = True

timeup = Text(text="Time (min):", x=-1.2, y=0.27, size=0.02, font='assets/fonts/SpaceMono-Regular.ttf')
timelabel = Text(text=str(times[0]), x=-1.2, y=0.23, font='assets/fonts/SpaceMono-Regular.ttf', size=0.04)
timelabel._eternal = True
timeup._eternal = True

key1 = Text(text="Color Key (Phases):", x=-1.2, y=0.15, size=0.02, font='assets/fonts/SpaceMono-Regular.ttf')

key2a = Text(text="Launch:", x=-1.2, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key2b = Text(text="Red", x=-1.05, y=0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03, color=color.red)

key3a = Text(text="Initital Firing:", x=-1.2, y=0.05, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key3b = Text(text="Cyan", x=-0.95, y=0.05, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03, color=color.cyan)

key4a = Text(text="Orion Separation:", x=-1.2, y=0, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key4b = Text(text="Green", x=-0.9, y=0, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03, color=color.green)

key5a = Text(text="Subsequent Burning:", x=-1.2, y=-0.05, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key5b = Text(text="Gold", x=-0.9, y=-0.05, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03, color=color.gold)

key6a = Text(text="Life Systems Check:", x=-1.2, y=-0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key6b = Text(text="Pink", x=-0.9, y=-0.1, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03, color=color.pink)

key7a = Text(text="Burn Fuel:", x=-1.2, y=-0.15, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key7b = Text(text="Yellow", x=-1.05, y=-0.15, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03, color=color.yellow)

key8a = Text(text="Translunar Injection:", x=-1.2, y=-0.2, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key8b = Text(text="Blue", x=-0.87, y=-0.2, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03, color=color.blue)

key9a = Text(text="Translunar Outbound:", x=-1.2, y=-0.25, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key9b = Text(text="Brown", x=-0.89, y=-0.25, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03, color=color.brown)

key0a = Text(text="Return:", x=-1.2, y=-0.3, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key0b = Text(text="Azure", x=-1.05, y=-0.3, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03, color=color.azure)

key15a = Text(text="Landing:", x=-1.2, y=-0.35, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03)
key15b = Text(text="Lime", x=-1.05, y=-0.35, font='assets/fonts/SpaceMono-Regular.ttf', size=0.03, color=color.lime)

## POSSIBLE USE FOR DEBUG
# xlabel = Text(text="X: "+str(points[0][0]/0.000125),x=-0.75,y=0.47)
# xlabel._eternal = True
# ylabel = Text(text="Y: "+str(points[0][1]/0.000125),x=-0.75,y=0.4)
# ylabel._eternal = True
# zlabel = Text(text="Z: "+str(points[0][2]/0.000125),x=-0.75,y=0.34)
# zlabel._eternal = True

distances = []

antennas = [{'name': 'WPSA', 'value': 1000, 'color': color.red}, {'name': 'DS54', 'value': 800, 'color': color.blue},
            {'name': 'DS24', 'value': 600, 'color': color.green}, {'name': 'DS34', 'value': 400, 'color': color.orange}]

antennatitle = Text(text="Antenna priority", x=0.97, y=0, size=0.02, font='assets/fonts/SpaceMono-Regular.ttf')

antenna1 = Text(text="1) " + antennas[0]['name'] + " - " + str(antennas[0]['value']), x=0.9, y=-0.05, size=0.04,
                font='assets/fonts/SpaceMono-Regular.ttf', color=antennas[0]['color'])

antenna2 = Text(text="2) " + antennas[1]['name'] + " - " + str(antennas[1]['value']), x=0.9, y=-0.1, size=0.04,
                font='assets/fonts/SpaceMono-Regular.ttf', color=antennas[1]['color'])

antenna3 = Text(text="3) " + antennas[2]['name'] + " - " + str(antennas[2]['value']), x=0.9, y=-0.15, size=0.04,
                font='assets/fonts/SpaceMono-Regular.ttf', color=antennas[2]['color'])

antenna4 = Text(text="4) " + antennas[3]['name'] + " - " + str(antennas[3]['value']), x=0.9, y=-0.2, size=0.04,
                font='assets/fonts/SpaceMono-Regular.ttf', color=antennas[3]['color'])


#p_b = Button(icon='playbutton.png', scale=.25, x=0, y=-0.4, color=color.white)
#p_b.alpha = 0


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


def update():
    if held_keys['q']:
        app.quit()

    if ui_visible:
        editor_camera.enabled = False
        editor_camera.position = (0, 0, -10)
        editor_camera.rotation = (0, 0, 0)
        ui_on()
    else:
        editor_camera.enabled = True
        ui_off()

    global point_index, speed, points, distance, ci, pi, distances, phase, times, trajectory_line, model, current, inter, h
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
        orion.position = points[point_index]
        currents = points[point_index]
        if point_index + 1 == len(points):
            next = points[0]
        else:
            next = points[point_index + 1]

        if 8 <= times[point_index] < 48.23658:
            ci = 0
        elif 48.23658 <= float(times[point_index]) < 100.1082:
            ci = 1
            phase = "Initial firing"
        elif 100.1082 <= float(times[point_index]) < 196.0945:
            ci = 2
            phase = "Orion separates from ICPS"
        elif 196.0945 <= float(times[point_index]) < 283.6495:
            ci = 3
            phase = "Subsequent burning of fuel for higher orbit"
        elif 283.6495 <= float(times[point_index]) < 792.4494:
            ci = 4
            phase = "Life Systems Check/Orion USS Burn"
        elif 792.4494 <= float(times[point_index]) < 1487.65:
            ci = 5
            phase = "Life Systems Check/Burn Fuel"
        elif 1487.65 <= float(times[point_index]) < 6150.25142:
            ci = 6
            phase = "TransLunar Injection Propells to Moon"
        elif 6150.25142 <= float(times[point_index]) < 7200.25142:
            ci = 7
            phase = 'Translunar Outbound'
        elif 7200.25142 <= float(times[point_index]) < 10150.16998:
            ci = 8
            phase = 'Return to Earth'
        elif 12690 <= float(times[point_index]):
            ci = 9
            phase = 'Landing'

        if len(points) != point_index + 1:
            h = times[point_index + 1] - times[point_index]
            h *= 60
            h = h / 25960.633996

        model.position = Vec3(currents.x, currents.y, currents.z)  # clean_line(currents, next, inter)
        speed = overall_velocity[point_index]
        x, y, z = model.position
        x2, y2, z2 = next

        current.append(points[point_index + 1])

        distance += length(x, y, z, x2, y2, z2)
        distance = np.round(distance, 2)
        distances.append(distance)
        if point_index + 1 != len(points):
            a = Mesh(vertices=current, mode='line', thickness=2)
            trajectory_line.model = a
        #  trajectory_line.alpha = 0
        distancetotal.text = str(distance)
        timelabel.text = str(float(times[point_index]))
        phaselabel.text = phase
        # xlabel.text="X: "+str(round(points[point_index][0],5)/0.000125)
        # ylabel.text="Y: "+str(round(points[point_index][1],5)/0.000125)
        # zlabel.text="Z: "+str(round(points[point_index][2],5)/0.000125)
        if pi != ci:
            trajectory_line, current = create_trajectory_line(colors[ci], point_index, point_index + 1)
            pi = ci
        # print(ci)
        inter += speed * time.dt
        time.sleep(h)
        point_index += int(speed * len(points) / 5.3)
        # point_index += int(speed*len(points)/5.301)

        if inter >= 1.0:
            inter = 0
            point_index += 1
    else:
        point_index = 0
        speed = overall_velocity[0]
        distance = 0
        current = [points[0], points[1]]
        scene.clear()


class Planet:
    def __init__(self, scale, file, pos=(0, 0, 0)):
        self.entity = Entity(model="sphere", texture=file, scale=(scale, scale, scale), position=pos)


earth = Planet(12742 * scale_factor, "assets/textures-models/planet-textures/earth.jpg").entity
moon = Planet(3474 * scale_factor, "assets/textures-models/planet-textures/moon.jpg",
              pos=((-384400 * scale_factor) + 1, -16.25, -8)).entity
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


def place_marker(lat, lon, radius, color=color.white, scale=0.0005, parent=None, texture=None,
                 model=load_model('assets/textures-models/antenna-models/DSN_34.obj')):
    """Place a marker at the specified latitude and longitude on the sphere."""
    position = lat_lon_to_3d(lat, lon, radius)  # Exact surface position
    marker = Entity(model=model, scale=scale, parent=parent, color=color, position=position, texture=texture)
    return marker


antenna_locations = [
    (35.3399, -116.875),  # California
    (-35.5985, 148.982),  # Australia
    (40.5276, -4.5271),  # Spain
]
antennas = []
model_number = 0


for lat, lon in antenna_locations:
    antennas.append(place_marker(lat, lon, radius=0.5, color=color.white, scale=0.01, parent=earth,
                 model=antenna_models[model_number]))  # Attach antennas to Earth
    model_number += 1


"""
Be aware that `ui_objs` is when the home ui is showing.
`non_ui` is when the trajectory is showing.
"""

ui_objs = [logo, viewer_button, quit_button, play_button, viewer_text, play_text, quit_text, subtitle, menu_text, bg]
non_ui = [trajectory_line, earth, moon, space_bg, model, distanceup, phaseup, timeup, key1, antennatitle, antenna1, antenna2, antenna3,
          antenna4, distancetotal, phaselabel, timelabel]

for antenna in antennas:
    non_ui.append(antenna)

# add all 3 antennas

for num in ['2', '3', '4', '5', '6', '7', '8', '9', '0', '15']:
    for part in ['a', 'b']:
        exec(f"non_ui.append(key{num}{part})")
# add all the trajectory ui things

model_number = 0

def ui_on(manual=False):
    global ui_visible
    for obj in non_ui:
        obj.visible = False
    for ui in ui_objs:
        ui.visible = True
    ui_visible = True
    print("UI on") if not manual else print("FORCE BUTTON UI ON")


def ui_off(manual=False):
    global ui_visible
    for obj in non_ui:
        obj.visible = True
    for ui in ui_objs:
        ui.visible = False
    ui_visible = False
    print("UI off") if not manual else print("FORCE BUTTON UI OFF")

ui_on()


def start():
    app.run()

start()