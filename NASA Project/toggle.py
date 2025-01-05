# from ursina import *

# app = Ursina()

# camera = EditorCamera()


# class ToggleSwitch(Entity):
#     def __init__(self, position=(0, 0)):
#         super().__init__()


#         self.switch = Entity(
#             model='quad',  
#             color=color.blue,
#             scale=(2, 0.5), 
#             position=Vec2(position),
#             parent = scene,  
#             collider='box'
#         )


#         self.lever = Entity(
#             model='quad', 
#             color=color.green,
#             scale=(0.5, 1), 
#             position=Vec2(-0.75, 0), 
#             collider='box',
#             parent=self.switch  # Make the lever a child of the switch
#         )

#         self.cube = Entity(
#             model='cube',
#             color=color.orange,
#             scale=(0.5,1,1),
#             position=Vec3(0,-1,-1),
#         )

#         self.sphere = Entity(
#             model='sphere',
#             color=color.orange,
#             scale=(1,1,1),
#             position=Vec3(0,-1,-1)
#         )

#         self.is_on = True
    
#     def input(self, mouses):
#         # Check if mouse is clicked and if on the switch's area
#         if mouses == 'left mouse down' and self.switch.hovered:
          
#             self.is_on = not self.is_on
            
#             if self.is_on:
#                 self.lever.x = -0.75  
#                 self.lever.color = color.green  
#                 self.cube.alpha = 1
#                 self.sphere.alpha = 0
#             else:
#                 self.lever.x = 0.75  
#                 self.lever.color = color.red  
#                 self.cube.alpha = 0
#                 self.sphere.alpha = 1

#     def update(self):
        
#         self.switch.position = Vec2(self.switch.position.x, self.switch.position.y)
#         self.lever.position = Vec2(self.lever.position.x, self.lever.position.y)
        
        
#         self.switch.scale = (2, 0.5)  #
#         self.lever.scale = (0.5, 1)    



# toggle = ToggleSwitch(position=(0, 0))


# app.run()

from ursina import *

app = Ursina()

camera = EditorCamera()

class ToggleButton(Button):
    def __init__(self, position=(0, 0), **kwargs):
        super().__init__(**kwargs)
        

        self.scale = (0.1, 0.05) 
        self.position = position
        self.color = color.white  


        # Create the lever that will move from left to right
        self.lever = Button(
            model="quad",
            color=color.green,
            scale=(0.25, 0.8),  
            position=(-0.375, 0),  
            parent=self,
            text="",
            collider="box"
        )


        self.is_on = True


        self.cube = Entity(
            model='cube',
            color=color.orange,
            scale=(0.5, 1, 1),
            position=Vec3(0, -1, -1),
        )

        self.sphere = Entity(
            model='sphere',
            color=color.orange,
            scale=(1, 1, 1),
            position=Vec3(0, -1, -1)
        )

        self.cube.alpha = 0  
        self.sphere.alpha = 1  

    def on_click(self):

        self.is_on = not self.is_on

        if not self.is_on:

            self.lever.position = (0.375, 0)
            self.lever.color = color.red
            self.color = color.white 
            self.cube.alpha = 1  
            self.sphere.alpha = 0  
        else:
          
            self.lever.position = (-0.375, 0)
            self.lever.color = color.green  
            self.color = color.white  
            self.cube.alpha = 0  
            self.sphere.alpha = 1  


toggle_button = ToggleButton(position=(0, 0))


app.run()
