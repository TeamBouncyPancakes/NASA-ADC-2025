import pandas as pd
from ursina import *

def create_trajectory_line(csv_file):
    ms_data = pd.read_csv(csv_file)
    scale_factor = 0.000125
    points = [Vec3(x,y,z) * scale_factor for x, y, z in zip(ms_data['Rx(km)[J2000-EARTH]'],ms_data['Ry(km)[J2000-EARTH]'],ms_data['Rz(km)[J2000-EARTH]'])]

    line = Entity(model=Mesh(vertices=points, mode='line', thickness=2), color=color.red)
    return points, line

app = Ursina(size=(2500,1000))

index = 1

points, trajectory_line = create_trajectory_line('middle-school-data.csv')


camera.position = Vec3(0,0,-10)
camera.look_at(points[500])


editor_camera = EditorCamera(pan_speed = 1000)

camera.fov = 155

def update():
    global index, points
    if index < len(points):
        camera.look_at(points[index])
        index+=1
    # WASD camera movement
    if held_keys['w']: editor_camera.position += editor_camera.forward * time.dt * 5  # Move forward
    if held_keys['s']: editor_camera.position -= editor_camera.forward * time.dt * 5  # Move backward
    if held_keys['a']: editor_camera.position -= editor_camera.right * time.dt * 5    # Move left
    if held_keys['d']: editor_camera.position += editor_camera.right * time.dt * 5    # Move right
    if held_keys['q']: editor_camera.position += editor_camera.up * time.dt * 5       # Move up
    if held_keys['e']: editor_camera.position -= editor_camera.up * time.dt * 5       # Move down


app.run()