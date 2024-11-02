from ursina import *

# Initialize the Ursina app
app = Ursina()

# Menu visibility flag
menu_visible = True

# Create the main camera (standard view)
main_camera = EditorCamera(enabled = True)

# Create a second camera for a different view
side_camera = EditorCamera(enabled=False)  # Start with side camera disabled
side_camera.position = (5, 5, -5)  # Position the side camera at an angle
side_camera.rotation = (30, 45, 0)  # Rotate for a different view


# Create a whitelight source
whitelight = Light(parent=main_camera)  # Attach the whitelight to the main camera
whitelight.position = (2, 4, 2)  # Position the whitelight above and in front of the cube

# Create a cube
cube = Entity(
    
    model='cube',
    color=color.orange,
    position=(0, 0, 0),  # Centered in the scene
    scale=(1, 1, 1)
)

# Create a ground plane
ground = Entity(
    
    model='plane',
    color=color.green,
    scale=(20, 1, 20),  # Scale the ground to be large
    position=(0, 0, 0)  # Center the ground
)

# Menu text
menu_text = Text(
    
    text='Team Bouncy Pancakes',
    position=(-0.5, 0.4),  # Centered horizontally, slightly higher vertically
    scale=2
)

# Play button
play_button = Button(
    
    text='Play',
    scale=(0.2, 0.1),  # Size of the button
    position=(-0.1, 0),  # Centered horizontally, below the menu text
    on_click=lambda: start_game()  # Function to call when clicked
)

# Quit button
quit_button = Button(
    
    text='Quit',
    scale=(0.2, 0.1),
    position=(-0.1, -0.2),  # Centered horizontally, below the play button
    on_click=application.quit  # Quit the application
)

def start_game():
    global menu_visible
    menu_visible = False
    # Disable the menu components
    menu_text.disable()
    play_button.disable()
    quit_button.disable()

def update():
    """Update player movement and camera switching."""
    # Only check for camera switch if the menu is not visible
    if not menu_visible:
        # Rotate the cube for better visibility
        cube.rotation_y += 30 * time.dt  # Rotate cube for visual effect

        # Switch camera view when space bar is pressed
        if held_keys['space']:
            main_camera.enabled = not main_camera.enabled
            side_camera.enabled = not side_camera.enabled

# Run the Ursina app
app.run()