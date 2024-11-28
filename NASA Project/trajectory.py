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

model = Entity(model='assets/textures-models/orion-models/orion3.obj', scale=(1, 1, 1), color=color.light_gray)


index = 1

points, trajectory_line = create_trajectory_line()


editor_camera = EditorCamera(pan_speed = 1000)

camera.fov = 155

point_index = 0
overall_velocity = overall_velocity * 0.001
speed = overall_velocity[0]
distance = 0
phase = "Launch"

distancetotal = Text(text='Distance Travelled (km): '+str(distance),x=0.55,y=0.47,size=0.04)
phaselabel = Text(text='Phase: '+phase,x=-0.55,y=0.47,size=0.04)
timelabel = Text(text="Time (min): "+str(times[0]),x=-0.55,y=0.4)
xlabel = Text(text="X: "+str(points[0][0]),x=-0.75,y=0.47)
ylabel = Text(text="Y: "+str(points[0][1]),x=-0.75,y=0.4)
zlabel = Text(text="Z: "+str(points[0][2]),x=-0.75,y=0.34)

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

def lerp(p1, p2, t):
    x = (1-t) * p1
    y = p2 * t 
    return x + y
def clean_line(current,next,f):
    x = lerp(current.x,next.x,f)
    y = lerp(current.y,next.y,f)
    z = lerp(current.z,next.z,f)

    return Vec3(x,y,z)

inter = 0.75

def update():
    global point_index, speed, points, distance, current, inter, colors,times,ci,phase
    # WASD camera movement
    if held_keys['w']: editor_camera.position += editor_camera.forward * time.dt * 5  # Move forward
    if held_keys['s']: editor_camera.position -= editor_camera.forward * time.dt * 5  # Move backward
    if held_keys['a']: editor_camera.position -= editor_camera.right * time.dt * 5    # Move left
    if held_keys['d']: editor_camera.position += editor_camera.right * time.dt * 5    # Move right
    if held_keys['q']: editor_camera.position += editor_camera.up * time.dt * 5       # Move up
    if held_keys['e']: editor_camera.position -= editor_camera.up * time.dt * 5       # Move down

    if point_index < len(points):
        currents = points[point_index]
        if point_index + 1 == len(points):
            next = points[0]
        else:
            next = points[point_index+1]

        

        if 8 <= times[point_index] < 48.23658:
            ci = 0
        elif 48.23658 <= float(times[point_index]) < 100.1082:
            ci = 1
            phase = "Initial firing to get into a higher Orbit"
        elif 100.1082 <= float(times[point_index]) < 196.0945:
            ci = 2
            phase = "Orion separates from ICPS"
        elif 196.0945 <= float(times[point_index]) < 283.6495:
            ci = 3
            phase = "Subsequent burning of fuel for higher orbit"
        elif 283.6495 <= float(times[point_index]) < 792.4494:
            ci = 4
            phase = "Burn Fuel"
        elif 792.4494 <= float(times[point_index]) < 1487.65:
            ci = 5
            phase = "Burn Fuel"
        elif 1487.65 <= float(times[point_index]):
            ci = 6
            phase = "TransLunar Injection Burn Fuel"

        model.position = clean_line(currents, next, inter)
        speed = overall_velocity[point_index]
        x,y,z = model.position
        x2,y2,z2 = next

        current.append(points[point_index + 1])

        distance += length(x,y,z,x2,y2,z2)
        distance = np.round(distance, 2)

        a = Mesh(vertices=current, mode='line', thickness=2)
        trajectory_line.model = a
        distancetotal.text = 'Distance Travelled (km): '+str(distance)
        timelabel.text = 'Time (min): '+str(float(times[point_index]))
        phaselabel.text = 'Phase: '+phase
        xlabel.text="X: "+str(round(points[point_index][0],5))
        ylabel.text="Y: "+str(round(points[point_index][1],5))
        zlabel.text="Z: "+str(round(points[point_index][2],5))

        trajectory_line.color = colors[ci]
        print(ci)

        inter += speed * time.dt
        point_index += int(speed*len(points)/5.301)

        

        if inter >= 1.0:
            inter = 0
            point_index += 1
    else:
        point_index = 0
        speed = overall_velocity[0]
        distance = 0
        current = [points[0],points[1]]
        

class Planet:
    def __init__(self, scale, file, pos=(0, 0, 0)):
        self.entity = Entity(model="sphere", texture=file, scale=(scale, scale, scale), position=pos)
earth = Planet(2, "assets/textures-models/planet-textures/earth.jpg").entity
moon = Planet(0.54, "assets/textures-models/planet-textures/moon.jpg", pos=(-384400 * scale_factor, -17, -5)).entity
earth.cull_faces, earth.double_sided = False, True
moon.cull_faces, moon.double_sided = False, True
space_bg = Sky(texture="assets/textures-models/space-textures/space4.jpg")


app.run()