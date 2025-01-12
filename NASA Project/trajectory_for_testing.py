import pandas as pd
from ursina import *
import numpy as np
import time


ms_data = pd.read_csv('middle-school-data.csv')

x_velocity = ms_data['Vx(km/s)[J2000-EARTH]'].to_numpy()
y_velocity = ms_data['Vy(km/s)[J2000-EARTH]'].to_numpy()
z_velocity = ms_data['Vz(km/s)[J2000-EARTH]'].to_numpy()

times = ms_data['MISSION ELAPSED TIME (min)'].to_numpy()

test = np.array(x_velocity**2 + y_velocity**2 + z_velocity**2)

overall_velocity = np.array(np.sqrt(test))

colors = [color.red,color.cyan,color.green,color.gold,color.pink,color.yellow,color.orange,color.brown,color.azure,color.lime]


ci = 0

def lerp(p1, p2, t):
    x = (1-t) * p1
    y = p2 * t 
    a = x + y
    return a

points = [Vec3(a,b,s) * 0.000125 for a, b, s in zip(ms_data['Rx(km)[J2000-EARTH]'],ms_data['Ry(km)[J2000-EARTH]'],ms_data['Rz(km)[J2000-EARTH]'])]

def create_trajectory_line(c,x,y):
    global ci, points
    scale_factor = 0.000125

    

    current = [points[x],points[y]]
    line = Entity(model=Mesh(vertices=current, mode='line', thickness=2), color=c)
    return line, current

app = Ursina(size=(1000,500))

model = Entity(model='sphere', scale = (1,1,1),color=color.green)
model._eternal = True



index = 1

trajectory_line, current = create_trajectory_line(colors[ci],0,1)



point_index = 0
overall_velocity = overall_velocity * 0.001
speed = overall_velocity[0]
distance = 0
phase = "Launch"

distanceup = Text(text="Distance Travelled (km):",x=-0.97,y=0.37,size=0.02,font='assets/fonts/SpaceMono-Regular.ttf')
distancetotal = Text(text=str(distance),x=-0.97,y=0.33,size=0.04,font='assets/fonts/SpaceMono-Regular.ttf')
distancetotal._eternal = True
distanceup._eternal = True

phaseup = Text(text='Phase:',x=-0.97,y=0.47,size=0.02,font='assets/fonts/SpaceMono-Regular.ttf')
phaselabel = Text(text=phase,x=-0.97,y=0.43,size=0.04,font='assets/fonts/SpaceMono-Regular.ttf')
phaselabel._eternal = True
phaseup._eternal = True

timeup = Text(text="Time (min):",x=-0.97,y=0.27,size=0.02,font='assets/fonts/SpaceMono-Regular.ttf')
timelabel = Text(text=str(times[0]),x=-0.97,y=0.23,font='assets/fonts/SpaceMono-Regular.ttf',size=0.04)
timelabel._eternal = True
timeup._eternal = True

wh = Entity(model = 'quad',color=color.white,scale=(10.5,9),position=(-69,10,5))



key1 = Text(text="Color Key (Phases):",x=-0.97,y=0.15,size=0.02,font='assets/fonts/SpaceMono-Regular.ttf')

key2a = Text(text="Launch:",x=-0.97,y=0.1,font='assets/fonts/SpaceMono-Regular.ttf',size=0.03)
key2b = Entity(model='quad',color=color.red,scale = (6,6),position=(-55,8,0))

key2a.alpha = 1
key2b.alpha = 1

key3a = Text(text="Initital Firing:",x=-0.97,y=0.1,font='assets/fonts/SpaceMono-Regular.ttf',size=0.03)
key3b = Entity(model='quad',color=color.cyan,scale = (6,6),position=(-55,8,0))


key3a.alpha = 0
key3b.alpha = 0

key4a = Text(text="Orion Separation:",x=-0.97,y=0.1,font='assets/fonts/SpaceMono-Regular.ttf',size=0.03)
key4b = Entity(model='quad',color=color.green,scale = (6,6),position=(-55,8,0))

key4a.alpha = 0
key4b.alpha = 0

key5a = Text(text="Subsequent Burning:",x=-0.97,y=0.1,font='assets/fonts/SpaceMono-Regular.ttf',size=0.03)
key5b = Entity(model='quad',color=color.gold,scale = (6,6),position=(-55,8,0))

key5a.alpha = 0
key5b.alpha = 0

key6a = Text(text="Life Systems Check:",x=-0.97,y=0.1,font='assets/fonts/SpaceMono-Regular.ttf',size=0.03)
key6b = Entity(model='quad',color=color.pink,scale = (6,6),position=(-55,8,0))

key6a.alpha = 0
key6b.alpha = 0

key7a = Text(text="Burn Fuel:",x=-0.97,y=0.1,font='assets/fonts/SpaceMono-Regular.ttf',size=0.03)
key7b = Entity(model='quad',color=color.yellow,scale = (6,6),position=(-55,8,0))

key7a.alpha = 0
key7b.alpha = 0

key8a = Text(text="Translunar Injection:",x=-0.97,y=0.1,font='assets/fonts/SpaceMono-Regular.ttf',size=0.02)
key8b = Entity(model='quad',color=color.orange,position=(-55,8,0),scale = (6,6))

key8a.alpha = 0
key8b.alpha = 0

key9a = Text(text="Translunar Outbound:",x=-0.97,y=0.1,font='assets/fonts/SpaceMono-Regular.ttf',size=0.03)
key9b = Entity(model='quad',color=color.brown,scale = (6,6),position=(-55,8,0))


key9a.alpha = 0
key9b.alpha = 0

key0a = Text(text="Return:",x=-0.97,y=0.1,font='assets/fonts/SpaceMono-Regular.ttf',size=0.03)
key0b = Entity(model='quad',color=color.azure,scale = (6,6),position=(-55,8,0))


key0a.alpha = 0
key0b.alpha = 0

key15a = Text(text="Landing:",x=-0.97,y=0.1,font='assets/fonts/SpaceMono-Regular.ttf',size=0.03)
key15b = Entity(model='quad',color=color.lime,scale = (6,6),position=(-55,8,0))


key15a.alpha = 0
key15b.alpha = 0

keys = {key2a:key2b,key3a:key3b,key4a:key4b,key5a:key5b,key6a:key6b,key7a:key7b,key8a:key8b,key9a:key9b,key0a:key0b,key15a:key15b}

## POSSIBLE USE FOR DEBUG
# xlabel = Text(text="X: "+str(points[0][0]/0.000125),x=-0.75,y=0.47)
# xlabel._eternal = True
# ylabel = Text(text="Y: "+str(points[0][1]/0.000125),x=-0.75,y=0.4)
# ylabel._eternal = True
# zlabel = Text(text="Z: "+str(points[0][2]/0.000125),x=-0.75,y=0.34)
# zlabel._eternal = True

distances = []

antennas = [{'name':'WPSA','value':1000,'color':color.red},{'name':'DS54','value':800,'color':color.azure},{'name':'DS24','value':600,'color':color.green},{'name':'DS34','value':400,'color':color.orange}]

antennatitle = Text(text="Antenna priority",x=0.7,y=0,size=0.02,font='assets/fonts/SpaceMono-Regular.ttf')

antenna1 = Text(text="1) "+antennas[0]['name']+" - "+str(antennas[0]['value']),x=0.65,y=-0.05,size=0.04,font='assets/fonts/SpaceMono-Regular.ttf',color=antennas[0]['color'])

antenna2 = Text(text="2) "+antennas[1]['name']+" - "+str(antennas[1]['value']),x=0.65,y=-0.1,size=0.04,font='assets/fonts/SpaceMono-Regular.ttf',color=antennas[1]['color'])

antenna3 = Text(text="3) "+antennas[2]['name']+" - "+str(antennas[2]['value']),x=0.65,y=-0.15,size=0.04,font='assets/fonts/SpaceMono-Regular.ttf',color=antennas[2]['color'])

antenna4 = Text(text="4) "+antennas[3]['name']+" - "+str(antennas[3]['value']),x=0.65,y=-0.2,size=0.04,font='assets/fonts/SpaceMono-Regular.ttf',color=antennas[3]['color'])

# p_b = Button(icon='playbutton.png',scale=.25,x=0,y=-0.4,color=color.white)
# p_b.alpha = 0


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


# loading orion modules
slsbody = load_model('assets/textures-models/orion-models/orion_nasa_sls_body.glb')
slsbody_entity = Entity(model = slsbody, scale = (0.12,0.12,0.12))
slsbody_entity.rotation_z = 180
slsbody_entity.y = 0.45
slsnose = load_model('assets/textures-models/orion-models/orionmpcv.glb')
slsnose_entity = Entity(model = slsnose, scale = (0.12,0.12,0.12))
slsnose_entity.y = 10
icps = load_model('assets/textures-models/orion-models/icpstextured.glb')
service_module = load_model('assets/textures-models/orion-models/servicemoduletextured.glb')
capsule = load_model('assets/textures-models/orion-models/orioncapsuletextured.glb')
capsule_entity = Entity(model=capsule, position=(-1.8,3.21,-0.4))
service_module_entity = Entity(model=service_module, scale = 1, position=(-3.5,1.2,0))
orion = Entity(scale = (0.2,0.2,0.2))
orion.position=(0, 0, 0)
capsule_entity.parent = orion
service_module_entity.parent = orion
icps_entity = Entity(model=icps, scale=0.008, position = (-0.33,0.3,0))
icps_entity.rotation_x = -90
orion_maste = Entity(scale = (1,1,1))
icps_entity.parent = orion_maste
orion.parent = orion_maste
# sls.parent = orion_maste   
orion_maste.y = 9.8
orion_maste.x = 0.33
g_scale =0.2
orion_master = Entity(scale = (g_scale,g_scale,g_scale))
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

#points = points_array

def separate(e1,e2):
        e1.parent = None
        e2.parent = None

def translate_orion(e , x , y , z):
     e.x += x
     e.y += y
     e.z += z

ambient_light = AmbientLight()
ambient_light.intensity = 0.5

def update():

    if held_keys['z']:
        camera.fov = 90
    else:
        camera.fov = 155

    global point_index, speed, points, distances, current, inter, colors,times,ci,phase, trajectory_line, distance
    # WASD camera movement
    # if held_keys['w']: editor_camera.position += editor_camera.forward * time.dt * 5  # Move forward
    # if held_keys['s']: editor_camera.position -= editor_camera.forward * time.dt * 5  # Move backward
    # if held_keys['a']: editor_camera.position -= editor_camera.right * time.dt * 5    # Move left
    # if held_keys['d']: editor_camera.position += editor_camera.right * time.dt * 5    # Move right
    # if held_keys['q']: editor_camera.position += editor_camera.up * time.dt * 5       # Move up
    # if held_keys['e']: editor_camera.position -= editor_camera.up * time.dt * 5       # Move down
    pi = 0

    if point_index < len(points):
        currents = points[point_index+2]
        previous = points[point_index]
        if point_index + 1 == len(points):
            next = points[0]
        else:
            next = points[point_index+1]

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


        if 8 <= times[point_index] < 48.23658:
            ci = 0
            y = list(keys.items())
            m,n = y[ci]
            m.alpha = 1
            n.alpha = 1
            k,i = y[ci-1]
            k.alpha = 0
            i.alpha = 0
        elif 48.23658 <= float(times[point_index]) < 100.1082:
            ci = 1
            phase = "Initial firing"
            y = list(keys.items())
            m,n = y[ci]
            m.alpha = 1
            n.alpha = 1
            k,i = y[ci-1]
            k.alpha = 0
            i.alpha = 0

        elif 100.1082 <= float(times[point_index]) < 196.0945:
            ci = 2
            phase = "Orion separates from ICPS"
            y = list(keys.items())
            m,n = y[ci]
            m.alpha = 1
            n.alpha = 1
            k,i = y[ci-1]
            k.alpha = 0
            i.alpha = 0
        elif 196.0945 <= float(times[point_index]) < 283.6495:
            ci = 3
            phase = "Subsequent burning of fuel for higher orbit"
            y = list(keys.items())
            m,n = y[ci]
            m.alpha = 1
            n.alpha = 1
            k,i = y[ci-1]
            k.alpha = 0
            i.alpha = 0
        elif 283.6495 <= float(times[point_index]) < 792.4494:
            ci = 4
            phase = "Life Systems Check/Orion USS Burn"
            y = list(keys.items())
            m,n = y[ci]
            m.alpha = 1
            n.alpha = 1
            k,i = y[ci-1]
            k.alpha = 0
            i.alpha = 0
        elif 792.4494 <= float(times[point_index]) < 1487.65:
            ci = 5
            phase = "Life Systems Check/Burn Fuel"
            y = list(keys.items())
            m,n = y[ci]
            m.alpha = 1
            n.alpha = 1
            k,i = y[ci-1]
            k.alpha = 0
            i.alpha = 0
        elif 1487.65 <= float(times[point_index]) < 6150.25142:
            ci = 6
            phase = "TransLunar Injection Propells to Moon"
            y = list(keys.items())
            m,n = y[ci]
            m.alpha = 1
            n.alpha = 1
            k,i = y[ci-1]
            k.alpha = 0
            i.alpha = 0
        elif 6150.25142 <= float(times[point_index]) < 7200.25142:
            ci = 7
            phase = 'Translunar Outbound'
            y = list(keys.items())
            m,n = y[ci]
            m.alpha = 1
            n.alpha = 1
            k,i = y[ci-1]
            k.alpha = 0
            i.alpha = 0
        elif 7200.25142 <= float(times[point_index]) < 10150.16998:
            ci = 8
            phase = 'Return to Earth'
            y = list(keys.items())
            m,n = y[ci]
            m.alpha = 1
            n.alpha = 1
            k,i = y[ci-1]
            k.alpha = 0
            i.alpha = 0
        elif 12690 <= float(times[point_index]):
            ci = 9
            phase = 'Landing'
            y = list(keys.items())
            m,n = y[ci]
            m.alpha = 1
            n.alpha = 1
            k,i = y[ci-1]
            k.alpha = 0
            i.alpha = 0
        if len(points) != point_index+1:
            h = times[point_index+1] - times[point_index]
            h *= 60
            h = h/25960.633996

        if ci >=2:
            separate(slsnose_entity, slsbody_entity)
            slsnose_entity.z -= 0.5
            slsbody_entity.z -= 0.5
            orion_maste.position=Vec3(0,0,0)

        if ci>=6:
            icps_entity.parent=None
            icps_entity.z -= 0.5
            orion_maste.position=Vec3(0,0,0)

        if ci>=9:
            capsule_entity.parent=None
            capsule_entity.z -= 0.1
            capsule_entity.rotation_x = 0.1
            orion_maste.position=Vec3(0,0,0)



        
        orion_master.position =  Vec3(currents.x-0.05,currents.y+0.07,currents.z+0.05) #clean_line(currents, next, inter)
        if held_keys['z']:
            camera.position=Vec3(orion_master.x, orion_master.y, orion_master.z-1.5)
        speed = overall_velocity[point_index]
        x,y,z = orion_master.position
        x2,y2,z2 = next

    
    

        current.append(points[point_index + 1])

        distance += length(x,y,z,x2,y2,z2)
        distance = np.round(distance, 2)
        distances.append(distance)
        if point_index+1 != len(points):
            a = Mesh(vertices=current, mode='line', thickness=2)
            trajectory_line.model = a
          #  trajectory_line.alpha = 0
        distancetotal.text = str(distance)
        timelabel.text = str(float(times[point_index]))
        phaselabel.text = phase
        # xlabel.text="X: "+str(round(points[point_index][0],5)/0.000125)
        # ylabel.text="Y: "+str(round(points[point_index][1],5)/0.000125)
        # zlabel.text="Z: "+str(round(points[point_index][2],5)/0.000125)
        # if pi != ci:
        trajectory_line, current = create_trajectory_line(colors[ci],point_index,point_index+1)
            # pi = ci
        # print(ci)

        

        inter += speed * time.dt
        time.sleep(h)
        point_index += int(speed*len(points)/5.3)
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
