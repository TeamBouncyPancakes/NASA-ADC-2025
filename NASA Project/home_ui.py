from ursina import *
app = Ursina(size=(1000, 500))

font_size = 50
title = Text(text='Team Bouncy Pancakes', world_scale=1, font='assets/fonts/PlexSans/Regular.ttf')
title.size = .025
title.position = (0, 0)

def update():
    if held_keys['esc'] or held_keys['q']:
        quit()

editor_camera = EditorCamera(pan_speed = 1000)

camera.fov = 155
app.run()
