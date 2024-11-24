import numpy as np
from ursina import *
from PIL import Image
from math import sin, cos, radians
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader, unlit_shader
import pandas as pd
import time

from scipy.ndimage import median_filter

app = Ursina(size=(2500,1000))



ms_data = pd.read_csv('middle-school-data.csv')

x_velocity = ms_data['Vx(km/s)[J2000-EARTH]'].to_numpy()
y_velocity = ms_data['Vy(km/s)[J2000-EARTH]'].to_numpy()
z_velocity = ms_data['Vz(km/s)[J2000-EARTH]'].to_numpy()

times = ms_data['MISSION ELAPSED TIME (min)'].to_numpy()

test = np.array(x_velocity**2 + y_velocity**2 + z_velocity**2)

overall_velocity = np.array(np.sqrt(test))

colors = [color.red,color.cyan,color.green,color.gold,color.pink,color.yellow,color.blue]

c = 0

slsbody = load_model('assets/textures-models/orion-models/body_sls.obj')
# slsbodytext = load_texture('assets/textures-models/orion-models/body_sls.mtl')

slsbody_entity = Entity(model = slsbody, texture = 'assets/textures-models/orion-models/body_sls.mtl', scale = (0.12,0.12,0.12))
slsbody_entity.rotation_z = 180
slsbody_entity.y = 0.45
slsnose = load_model('assets/textures-models/orion-models/orion_mpcv.obj')
# slsnosetext = load_texture('assets/textures-models/orion-models/orion_mpcv.mtl')
slsnose_entity = Entity(model = slsnose, texture = 'assets/textures-models/orion-models/orion_mpcv.mtl', scale = (0.12,0.12,0.12))
slsnose_entity.y = 10
icps = load_model('assets/textures-models/orion-models/icps.obj')
service_module = load_model('assets/textures-models/orion-models/orion_service_module.obj')
capsule = load_model('assets/textures-models/orion-models/orion_capsule_new.obj')
capsule_entity = Entity(model=capsule, position=(0,0,0))
service_module_entity = Entity(model=service_module, scale = 1, position=(0,1.2,0))
orion = Entity(scale = (0.2,0.2,0.2))
orion.position=(0, 0, 0)
capsule_entity.parent = orion
service_module_entity.parent = orion
icps_entity = Entity(model=icps, texture = 'assets/textures-models/orion-models/icps.mtl', scale=0.008, position = (-0.33,0.3,0))
icps_entity.rotation_x = -90
orion_maste = Entity(scale = (1,1,1))
icps_entity.parent = orion_maste
orion.parent = orion_maste
# sls.parent = orion_maste   
orion_maste.y = 9.8
orion_maste.x = 0.33
orion_master = Entity(scale = (0.09,0.09,0.09))
slsbody_entity.parent = orion_master
slsnose_entity.parent = orion_master
orion_maste.parent = orion_master
# orion_master.z = -0.5
slsbody_entity.rotation_y = 90
orion_master.rotation_z = -90
light = DirectionalLight(parent=orion_master)
light.look_at(orion_master)

ci = 0

def lerp(p1, p2, t):
    x = (1-t) * p1
    y = p2 * t 
    a = x + y
    return a

points = [Vec3(a,b,s) * 0.000125 for a, b, s in zip(ms_data['Rx(km)[J2000-EARTH]'],ms_data['Ry(km)[J2000-EARTH]'],ms_data['Rz(km)[J2000-EARTH]'])]
print(points[1])
def create_trajectory_line(c,x,y):
    global ci, points
    scale_factor = 0.000125

    

    current = [points[x],points[y]]
    line = Entity(model=Mesh(vertices=current, mode='line', thickness=2), color=c)
    return line, current





index = 1

trajectory_line, current = create_trajectory_line(colors[ci],0,1)


editor_camera = EditorCamera(pan_speed = 1000)
 
camera.fov = 155

point_index = 0
overall_velocity = overall_velocity * 0.001
speed = overall_velocity[0]
distance = 0
phase = "Launch"

distancetotal = Text(text='Distance Travelled (km): '+str(distance),x=0.55,y=0.47,size=0.04)
distancetotal._eternal = True
phaselabel = Text(text='Phase: '+phase,x=-0.55,y=0.47,size=0.04)
phaselabel._eternal = True
timelabel = Text(text="Time (min): "+str(times[0]),x=-0.55,y=0.4)
timelabel._eternal = True
xlabel = Text(text="X: "+str(points[0][0]/0.000125),x=-0.75,y=0.47)
xlabel._eternal = True
ylabel = Text(text="Y: "+str(points[0][1]/0.000125),x=-0.75,y=0.4)
ylabel._eternal = True
zlabel = Text(text="Z: "+str(points[0][2]/0.000125),x=-0.75,y=0.34)
zlabel._eternal = True

distances = []



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


def clean_line(current,next,f):
    x = lerp(current.x,next.x,f)
    y = lerp(current.y,next.y,f)
    z = lerp(current.z,next.z,f)

    return Vec3(x,y,z)

inter = 0.75

def median_filter(points, window_size=3):
    smoothed_points = []
    for i in range(len(points)):
        # Define the window range: from max(0, i - window_size//2) to min(len(points), i + window_size//2)
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

points = points_array
print(points[1])

def separate(e1,e2):
        e1.parent = None
        e2.parent = None

def translate_orion(e , x , y , z):
     e.x += x
     e.y += y
     e.z += z


def update():
    global point_index, speed, points, distances, current, inter, colors,times,ci,phase, trajectory_line, distance
    # WASD camera movement
    if held_keys['w']: editor_camera.position += editor_camera.forward * time.dt * 5  # Move forward
    if held_keys['s']: editor_camera.position -= editor_camera.forward * time.dt * 5  # Move backward
    if held_keys['a']: editor_camera.position -= editor_camera.right * time.dt * 5    # Move left
    if held_keys['d']: editor_camera.position += editor_camera.right * time.dt * 5    # Move right
    if held_keys['q']: editor_camera.position += editor_camera.up * time.dt * 5       # Move up
    if held_keys['e']: editor_camera.position -= editor_camera.up * time.dt * 5       # Move down
    pi = 0

    light.look_at(orion_master)

    if point_index < len(points):
        currents = points[point_index+2]
        previous = points[point_index]
        #intergrating orion onto trajectory
        direction = (currents - previous).normalized()
        orion_master.position += direction * 1 * time.dt


        if direction.length() > 0:
            # Calculate the angle in radians
            target_rotation_y = math.degrees(math.atan2(direction.x, direction.y))
            orion_master.rotation_y = lerp(orion_master.rotation_y, target_rotation_y, 5 * time.dt)

            # Update the front's orientation to match the direction of movement
            tp = orion_master.position + direction
            orion_master.look_at(tp)
            if orion_master.rotation_y>0:
                orion_master.rotation_y+=90
            else:
                orion_master.rotation_y-=90

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
            phase = "Life Systems Check/Orion USS Burn"
        elif 792.4494 <= float(times[point_index]) < 1487.65:
            ci = 5
            phase = "Life Systems Check/Burn Fuel"
        elif 1487.65 <= float(times[point_index]):
            ci = 6
            phase = "TransLunar Injection Propells to Moon"

        if ci >=2:
            separate(slsnose_entity, slsbody_entity)
            slsnose_entity.z -= 0.5
            slsbody_entity.z -= 0.5
            orion_maste.position=Vec3(0,0,0)

        if ci>=6:
            icps_entity.parent=None
            icps_entity.z -= 0.5
            orion_maste.position=Vec3(0,0,0)


        orion_master.position =  Vec3(currents.x,currents.y,currents.z) #clean_line(currents, next, inter)
        speed = overall_velocity[point_index]
        x,y,z = orion_master.position
        x2,y2,z2 = next

        current.append(points[point_index + 1])

        distance += length(x,y,z,x2,y2,z2)
        distance = np.round(distance, 2)
        distances.append(distance)

        a = Mesh(vertices=current, mode='line', thickness=2)
        trajectory_line.model = a
        distancetotal.text = 'Distance Travelled (km): '+str(distance)
        timelabel.text = 'Time (min): '+str(float(times[point_index]))
        phaselabel.text = 'Phase: '+phase
        xlabel.text="X: "+str(round(points[point_index][0],5)/0.000125)
        ylabel.text="Y: "+str(round(points[point_index][1],5)/0.000125)
        zlabel.text="Z: "+str(round(points[point_index][2],5)/0.000125)
        if pi != ci:
            trajectory_line, current = create_trajectory_line(colors[ci],point_index,point_index+1)
            pi = ci
        # print(ci)

        inter += speed * time.dt
        point_index += 1
        # point_index += int(speed*len(points)/5.301)


        if inter >= 1.0:
            inter = 0
            point_index += 1
    else:
        point_index = 0
        speed = overall_velocity[0]
        distance = 0
        current = [points[0],points[1]]
        scene.clear()

        


app.run()