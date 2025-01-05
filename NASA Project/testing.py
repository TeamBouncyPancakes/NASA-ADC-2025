from ursina import *

app = Ursina()

# Create a square (quad) UI element
square = Entity(model='quad', scale=(0.1, 0.1), color=color.red, position=(0.45, 0.45), parent=camera.ui)

# Set up the camera and ensure it is in a valid state
camera.position = (0, 0, 5)
camera.rotation = (0, 0, 0)
camera.scale = (1, 1, 1)

# Enable the editor camera

editor_camera = EditorCamera(pan_speed=1000)

# Main update loop
def update():
    # You can add additional logic here, but the square will stay at the top-right corner
    if held_keys['w']: editor_camera.position += editor_camera.forward * time.dt * 5  # Move forward
    if held_keys['s']: editor_camera.position -= editor_camera.forward * time.dt * 5  # Move backward
    if held_keys['a']: editor_camera.position -= editor_camera.right * time.dt * 5  # Move left
    if held_keys['d']: editor_camera.position += editor_camera.right * time.dt * 5  # Move right
    if held_keys['q']: editor_camera.position += editor_camera.up * time.dt * 5  # Move up
    if held_keys['e']: editor_camera.position -= editor_camera.up * time.dt * 5  # Move down
    if held_keys["escape"]:
        quit()

app.run()
