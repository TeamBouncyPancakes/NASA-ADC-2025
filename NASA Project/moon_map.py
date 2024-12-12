
# Moon Map with Ursina


from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Create the moon
moon = Entity(model='sphere', texture='assets/textures-models/planet-textures/moon.jpg', scale=10)

# Create the south pole mini map
south_pole_mini_map = Sprite(model='cube', texture='moon.jpg', scale=2, position=(-5, 5, -5), parent=camera.ui)

# First Person Controller
player = EditorCamera()

def update():
    if held_keys['escape']:
        application.quit()

app.run()
