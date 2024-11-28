
# Moon Map with Ursina

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Create the moon
moon = Entity(model='sphere', texture='assets/textures-models/planet-textures/moon.jpg', scale=10)

# Create the south pole mini map
south_pole_mini_map = Entity(model='cube', texture='moon.jpg', scale=2, position=(-5, 5, -5))

# First Person Controller
player = FirstPersonController()

def update():
    if held_keys['escape']:
        application.quit()

app.run()
